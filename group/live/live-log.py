#!/usr/bin/env python3
"""Shared live log for every agent working in design-systems-09Oct26 (Claude Code and Cursor).

One script, called by both apps' hooks:
  record  after a file edit: appends one line to group/LIVE.md (written by the hook, not by the model's memory)
  inject  before each message: puts the last lines of group/LIVE.md in front of the agent about to answer
  guard   before a file edit: if ANOTHER agent session edited that same file in the last few minutes, stop once and say
          "re-read it first"; the next attempt goes through. It warns the next write; it is not a lock.

Usage: live-log.py <record|inject|guard|shellguard> [claude|cursor]   (hook JSON on stdin)
       live-log.py ready <claude|cursor> "what is finished"            (an agent: MY giving work is done and tested;
                                                                        another agent's is refused, ōkina can mark either)
       live-log.py check <claude|cursor|okina>                         (release-blue: is anyone else's work unfinished?)
       live-log.py released <claude|cursor|okina> <version>            (release-blue: record the release)
       live-log.py selftest                                            (checks the unfinished-work check on a scratch log)
A shell command that only runs the release/ready commands, node --check or read-only commands is logged as "run", not
"shell", and never counts as unfinished work (see harmless()).
shellguard (before a shell command): refuses a direct deploy of giving, the GIVING_RELEASE_BLUE override, and remote
database commands on the live database. The one way out is release-blue.command, which checks the others first.
It also refuses "live-log.py ready <the other agent>", and changing the marks that say who runs live-log.py (see caller()).
Claude Code: UserPromptSubmit -> inject, PreToolUse(Edit|Write|MultiEdit|NotebookEdit) -> guard, PostToolUse(same + Bash) -> record.
Cursor: beforeSubmitPrompt -> inject cursor, preToolUse -> guard cursor, afterFileEdit -> record cursor.
Every failure exits 0 with an empty answer, so a broken log never blocks work.
"""
import json
import os
import re
import shlex
import sys
import time

ROOT = os.path.realpath(os.environ.get("LIVE_LOG_ROOT", "/Users/okinaasagao/Desktop/consensorAI/design-systems-09Oct26"))
LOG = os.path.join(ROOT, "group", "LIVE.md")
STATE = os.path.join(ROOT, "group", "live", ".warned.json")
IGNORE = ("/.wrangler/", "/node_modules/", "/group/stages/", "/group/backups/", "/group/live/", "/group/LIVE.md", "/.git/")
SHOW_LINES, SHOW_HOURS, GUARD_SECONDS, MAX_LINES, SHELL_SHOWN = 14, 12, 600, 3000, 140
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
WRITE_HINT = re.compile(r"((?<![\d&])>>?(?!\s*(&|/dev/null))|sed -i|write_text|\.write\(|rsync|\bcp\b|\bmv\b|\btee\b|\brm\b|build\.py|mirror-green|release-blue|alert-agents)")
HEADER = "# giving live log\n\nOne line per edit, written by the agents' hooks (group/live/live-log.py). Newest at the bottom. Format: time | agent·session | what | file\n\n"


def out(obj):
    sys.stdout.write(json.dumps(obj) + "\n")


def who(payload, forced):
    agent = forced or ("cursor" if "cursor_version" in payload else "claude")
    sid = str(payload.get("session_id") or payload.get("conversation_id") or "")
    return agent, (agent + "·" + sid[:4]) if sid else agent


def rel(path):
    path = os.path.realpath(os.path.expanduser(path))
    return path[len(ROOT) + 1:] if path.startswith(ROOT + "/") else None


def watched(path):
    r = rel(path) if path else None
    return r if r and not any(x in "/" + r for x in IGNORE) else None


def find_path(obj):
    """The file a tool call writes, wherever the app put it."""
    if isinstance(obj, dict):
        for k in ("file_path", "path", "target_file", "filePath", "notebook_path", "file"):
            v = obj.get(k)
            if isinstance(v, str) and v:
                return v
        for v in obj.values():
            p = find_path(v)
            if p:
                return p
    return None


def lines():
    try:
        with open(LOG, encoding="utf-8") as f:
            return [l.rstrip("\n") for l in f if re.match(r"^\d{4}-\d\d-\d\d \d\d:\d\d:\d\d \| ", l)]
    except OSError:
        return []


def parse(line):
    try:
        ts, who_, what, path = [p.strip() for p in line.split(" | ", 3)]
        return time.mktime(time.strptime(ts, "%Y-%m-%d %H:%M:%S")), who_, what, path
    except Exception:
        return None


def record(payload, forced):
    _, me = who(payload, forced)
    tool = payload.get("tool_name") or ""
    if tool == "Bash" or tool == "Shell":
        cmd = str((payload.get("tool_input") or {}).get("command") or "")
        if not (ROOT in cmd or "publish/giving" in cmd or "group/" in cmd) or not WRITE_HINT.search(cmd):
            return
        # a new line shows as " ; " so the logged text keeps its command boundaries; a cut line ends in "…"
        shown = re.sub(r"\s+", " ", cmd.replace(ROOT + "/", "").replace("\\\n", " ").replace("\n", " ; "))
        target = "(shell) " + (shown[:SHELL_SHOWN] + "…" if len(shown) > SHELL_SHOWN else shown)
        try:
            what = "run" if harmless(cmd) else "shell"  # decided here, where the whole command is known
        except Exception:
            what = "shell"
    else:
        p = payload.get("file_path") or find_path(payload.get("tool_input") or {}) or find_path(payload)
        target, what = watched(p), "edit"
        if not target:
            return
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    last = parse(lines()[-1]) if lines() else None
    if last and last[1] == me and last[3] == target and time.time() - last[0] < 3:
        return  # the same edit reported twice (both apps' hook systems)
    if not os.path.exists(LOG):
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(HEADER)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{now} | {me} | {what} | {target}\n")
    all_lines = lines()
    if len(all_lines) > MAX_LINES:  # keep the log short; the older half moves to backups
        keep = all_lines[-MAX_LINES // 2:]
        os.makedirs(os.path.join(ROOT, "group", "backups"), exist_ok=True)
        with open(os.path.join(ROOT, "group", "backups", "LIVE-" + time.strftime("%Y%m%dT%H%M%S") + ".md"), "w", encoding="utf-8") as f:
            f.write("\n".join(all_lines[:-MAX_LINES // 2]) + "\n")
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(HEADER + "\n".join(keep) + "\n")


def inject(payload, forced):
    agent, me = who(payload, forced)
    places = [str(payload.get("cwd") or "")] + [str(r) for r in (payload.get("workspace_roots") or [])]
    here = any(p and (os.path.realpath(p) + "/").startswith(ROOT + "/") for p in places)
    recent = [l for l in lines() if (parse(l) or (0,))[0] > time.time() - SHOW_HOURS * 3600][-SHOW_LINES:]
    if not here or not recent:
        out({"continue": True} if agent == "cursor" else {})
        return
    text = ("Shared live log (group/LIVE.md): the latest edits by every agent in this project, newest last. "
            f"You are {me}. Before changing a file another session touched recently, re-read it.\n" + "\n".join(recent))
    if agent == "cursor":
        out({"continue": True, "additional_context": text})
    else:
        out({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": text}})


def guard(payload, forced):
    agent, me = who(payload, forced)
    allow = (lambda: out({"permission": "allow"})) if agent == "cursor" else (lambda: None)
    tool = payload.get("tool_name") or ""
    if agent == "claude" and tool not in EDIT_TOOLS:
        return allow()
    target = watched(find_path(payload.get("tool_input") or {}) or "")
    if not target:
        return allow()
    hit = None
    for l in reversed(lines()):
        e = parse(l)
        if not e or time.time() - e[0] > GUARD_SECONDS:
            break
        if e[3] == target and e[1] != me:
            hit = e
            break
    if not hit:
        return allow()
    try:
        warned = json.load(open(STATE))
    except Exception:
        warned = {}
    key = f"{me}|{target}|{int(hit[0])}"
    if warned.get(key):
        return allow()
    warned = {k: v for k, v in warned.items() if time.time() - v < 86400}
    warned[key] = time.time()
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(warned, f)
    ago = int(time.time() - hit[0])
    msg = (f"{hit[1]} edited {target} {ago}s ago (group/LIVE.md). Re-read the file now so you don't overwrite that edit, "
           "then make your change again. This check stops each edit once; the next attempt goes through.")
    if agent == "cursor":
        out({"permission": "deny", "agent_message": msg, "user_message": f"Paused one edit: {hit[1]} changed {target} {ago}s ago."})
    else:
        out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": msg}})


GIVING_SRC = ("publish/giving",)


def agent_of(who_):
    return who_.split("·", 1)[0]


def append(agent, what, text, by=None):
    if not os.path.exists(LOG):
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "w", encoding="utf-8") as f:
            f.write(HEADER)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {by or agent + '·cli'} | {what} | {text}\n")


# The marks each app puts in the environment of every shell command its agent runs (the hooks tag the same sessions as
# claude·xxxx / cursor·xxxx). Claude Code: CLAUDECODE=1 and CLAUDE_CODE_SESSION_ID. Cursor's agent: CURSOR_AGENT=1 and
# CURSOR_CONVERSATION_ID. A person in Terminal (ōkina, or release-blue.command double-clicked) has neither.
AGENT_ENV = {"claude": ("CLAUDECODE", "CLAUDE_CODE_SESSION_ID"), "cursor": ("CURSOR_AGENT", "CURSOR_CONVERSATION_ID")}
MARKS = r"(CLAUDECODE|CLAUDE_CODE_SESSION_ID|CURSOR_AGENT|CURSOR_CONVERSATION_ID)"
# setting or clearing those marks in the same command (FOO=…, unset FOO, env -i / env -u / env -)
WHO_ENV = re.compile(rf"(?<![\w$]){MARKS}=|\bunset\b[^|;&]*\b{MARKS}\b|\benv(\s+-\S+)*\s+(-[a-zA-Z]*[iu]\b|-(?=\s)|--ignore-environment|--unset)")
READY_FOR = re.compile(r"live-log\.py['\"]?\s+ready\s+['\"]?(claude|cursor)\b")


def caller(env=None):
    """(agent, who) for the one running this command: ('claude', 'claude·f217'), ('cursor', 'cursor·333b'),
    ('okina', 'okina') for a person, or (None, None) when both apps' marks are set and it can't tell."""
    env = os.environ if env is None else env
    found = [a for a, (mark, _) in AGENT_ENV.items() if env.get(mark, "") not in ("", "0")]
    if not found:
        return "okina", "okina"
    if len(found) > 1:
        return None, None
    sid = env.get(AGENT_ENV[found[0]][1], "")
    return found[0], found[0] + "·" + (sid[:4] or "cli")


def ready_refusal(target, agent):
    """Why `agent` may not mark `target`'s work ready, or None. Each agent marks only its own; ōkina marks either."""
    if agent in ("okina", target):
        return None
    if agent is None:
        return ("Not marked ready: this shell carries both Claude Code's and Cursor's marks, so it can't tell who is asking. "
                f"Mark your own work from your own app's shell, or ask ōkina to mark {target}'s work in Terminal.")
    return (f"Not marked ready: you are {agent}, and this would mark {target}'s work finished. Only {target} (or ōkina) "
            f"can say that; marking it for them let half-built work go live on 15 Oct. If ōkina wants a release now, tell "
            f"him {target}'s work isn't marked ready and ask him whether to wait for {target} or release anyway. "
            f"Your own work: python3 -I {ROOT}/group/live/live-log.py ready {agent} \"what\"")


# Shell commands that can't leave unreleased giving changes behind. The hook logs a shell command after it finishes, so
# Cursor's "node --check … && live-log.py ready … && ./release-blue.command cursor" lands after its own release and used to
# stop the next release as unfinished work. A command made only of the pieces below doesn't count. Anything else, or
# anything this can't follow ($(…), heredocs, writing to a file, VAR=…, subshells, an open quote), still counts.
SCRIPTS = {"release-blue.command", "mirror-green.command", "rollback-blue.command"}
WHO = ("claude", "cursor", "okina")
READ_ONLY = {"ls", "cat", "head", "tail", "wc", "grep", "egrep", "fgrep", "rg", "diff", "cmp", "stat", "file", "pwd", "echo",
             "date", "which", "true", "test", "[", "sleep", "ps", "du", "df", "cut", "tr", "basename", "dirname", "realpath",
             "readlink", "shasum", "md5", "sed", "find", "sort"}
# a command name among a read-only command's words: older log lines joined lines with spaces, so "ls x\nrm y" reads "ls x rm y"
WRITERS = {"sed", "perl", "python", "python3", "node", "ruby", "cp", "mv", "rm", "tee", "rsync", "ditto", "dd", "install",
           "touch", "mkdir", "ln", "chmod", "truncate", "patch", "git", "wrangler", "npm", "npx", "bash", "sh", "zsh", "tar",
           "unzip", "awk", "xargs", "curl", "open", "sqlite3"}
SEPARATORS = {"&&", "||", ";", "|", "&", "|&"}
TO_FILE = {">", ">>", ">|", "&>", "&>>"}


def commands(cmd):
    """The simple commands in a shell line, as word lists. None when it does something this can't follow."""
    if "$(" in cmd or "`" in cmd:
        return None
    lex = shlex.shlex(cmd.replace("\\\n", " ").replace("\n", " ; "), posix=True, punctuation_chars=True)
    lex.whitespace_split, lex.commenters = True, ""
    toks = list(lex)  # ValueError on an open quote
    found, cur, i = [], [], 0
    while i < len(toks):
        t, nxt = toks[i], (toks[i + 1] if i + 1 < len(toks) else "")
        if t in SEPARATORS:
            found.append(cur)
            cur = []
        elif t in TO_FILE or t in (">&", "<"):
            if not nxt.strip("();<>|&") or (t in TO_FILE and nxt != "/dev/null") or (t == ">&" and not nxt.isdigit()):
                return None  # only /dev/null, 2>&1 and reading a file are fine
            if cur and cur[-1].isdigit():
                cur.pop()  # the 2 of 2>/dev/null
            i += 1
        elif not t.strip("();<>|&"):
            return None  # <<, <<<, ( ), and anything else made only of operators
        else:
            cur.append(t)
        i += 1
    return [c for c in found + [cur] if c]


def harmless_command(words):
    head, args = words[0], words[1:]
    if "$" in head or "=" in head:
        return False  # VAR=… in front, or the command read from a variable
    name = head.rsplit("/", 1)[-1]
    if name == "cd":
        return len(args) <= 1
    if name in SCRIPTS:
        return len(args) <= 1 and (name != "release-blue.command" or not args or args[0] in WHO)
    if name == "node":
        return len(args) == 2 and args[0] in ("--check", "-c") and args[1].endswith((".js", ".mjs", ".cjs"))
    if name in ("python3", "python"):
        while args and re.fullmatch(r"-[IBEsu]+", args[0]):
            args = args[1:]
        if len(args) < 2 or "$" in args[0] or args[0].rsplit("/", 1)[-1] != "live-log.py":
            return False
        mode, rest = args[1], args[2:]
        if mode == "ready":
            return 1 <= len(rest) <= 2 and rest[0] in ("claude", "cursor")
        if mode in ("check", "released"):
            return len(rest) <= (1 if mode == "check" else 2) and (not rest or rest[0] in WHO)
        return mode == "selftest" and not rest
    if name not in READ_ONLY or any(a.rsplit("/", 1)[-1] in WRITERS for a in args):
        return False
    if name == "sed":  # sed -n 'N,Mp' only: -i, w and e write or run things
        opts, rest = [a for a in args if a.startswith("-")], [a for a in args if not a.startswith("-")]
        return "-n" in opts and set(opts) <= {"-n", "-E", "-r"} and bool(rest) and bool(re.fullmatch(r"(\d+|\$)(,(\d+|\$))?p", rest[0]))
    if name == "find":
        return not {"-exec", "-execdir", "-ok", "-okdir", "-delete", "-fprint", "-fprint0", "-fprintf", "-fls"} & set(args)
    if name == "sort":
        return not any(a.startswith("--output") or (a.startswith("-") and not a.startswith("--") and "o" in a) for a in args)
    return True


def cut_command(words):
    """The last command of a log line that was cut short: could it be the start of a harmless one?"""
    if harmless_command(words):
        return True
    head, args = words[0], words[1:]
    name = head.rsplit("/", 1)[-1]
    if "$" in head or "=" in head:
        return False
    if not args:  # cut inside the name, as in "… && ./rel"; a bare "r" could be rm or rsync, "./r" can't
        return len(name) >= (1 if "/" in head else 3) and any(s.startswith(name) for s in SCRIPTS)
    if name == "node":
        return len(args) <= 2 and len(args[0]) >= 3 and "--check".startswith(args[0])
    if name in ("python3", "python"):  # live-log.py never writes the giving source, whatever follows
        while args and re.fullmatch(r"-[IBEsu]+", args[0]):
            args = args[1:]
        script = args[0].rsplit("/", 1)[-1] if args else ""
        return bool(args) and "$" not in args[0] and (script == "live-log.py" or (len(args) == 1 and len(script) >= 4 and "live-log.py".startswith(script)))
    return False


def harmless(cmd, cut=False):
    """True when a shell command only runs the release and ready commands, node --check, or read-only commands.
    cut: the text was cut short in the log, so its last command may stop part-way through."""
    found = None
    for tail in ("", '"', "'") if cut else ("",):
        try:
            found = commands(cmd + tail)
            break
        except ValueError:  # an open quote
            continue
    if not found:
        return False
    return all(harmless_command(c) for c in found[:-1]) and (cut_command if cut else harmless_command)(found[-1])


def logged_harmless(target):
    """A 'shell' line already in the log: harmless as far as its text shows? The hook cuts long commands and marks the cut
    with '…' (counted: the hook saw the whole command and still logged 'shell'). Lines from before that marker were cut
    silently at 140 characters, so a line that long may stop part-way through its last command."""
    text = target[len("(shell) "):] if target.startswith("(shell) ") else target
    return not text.endswith("…") and harmless(text, cut=len(text) >= SHELL_SHOWN - 1)


def pending(releaser):
    """Edits to the giving source since the last release, by agents other than the releaser, with no later 'ready'.
    'run' lines and harmless 'shell' lines (release, ready, node --check, reading) are not edits."""
    entries = sorted((e for e in (parse(l) for l in lines()) if e), key=lambda e: e[0])
    last = max((i for i, e in enumerate(entries) if e[2] == "released"), default=-1)
    open_ = {}
    for e in entries[last + 1:]:
        ag = agent_of(e[1])
        if e[2] == "ready":
            open_.pop(ag, None)
        elif e[2] in ("edit", "shell") and ag != releaser and any(x in e[3] for x in GIVING_SRC):
            if e[2] == "shell" and logged_harmless(e[3]):
                continue
            open_.setdefault(ag, []).append(e)
    return open_


DEPLOY = re.compile(r"\bwrangler\b[^\n|;&]*\b(deploy|versions\s+(upload|deploy)|rollback|publish|delete)\b")
LIVE_DB = re.compile(r"\bd1\s+(migrations\s+apply|execute)\b[^\n|;&]*--remote")
OVERRIDE = re.compile(r"GIVING_RELEASE_BLUE\s*=")
SANCTIONED = re.compile(r"release-blue\.command|mirror-green\.command|rollback-blue\.command|Deploy giving\.command")


def ready_targets(cmd):
    """The agents a shell command marks ready with live-log.py. A quoted mention (grep "live-log.py ready …") doesn't count;
    a command this can't follow (heredoc, $(…), > file) is read by its text."""
    try:
        found = commands(cmd)
    except ValueError:
        found = None
    if found is None:
        return set(READY_FOR.findall(cmd))
    return {w[i + 2] for w in found for i in range(len(w) - 2)
            if w[i].rsplit("/", 1)[-1] == "live-log.py" and w[i + 1] == "ready" and w[i + 2] in AGENT_ENV}


def shellguard(payload, forced):
    agent, me = who(payload, forced)
    cmd = str(payload.get("command") or (payload.get("tool_input") or {}).get("command") or "")
    cwd = os.path.realpath(str(payload.get("cwd") or "/")) + "/"
    giving = any(x in cmd for x in ("publish/giving", "green-site", "consensor-giving")) or cwd.startswith(ROOT + "/publish/giving/") or cwd.startswith(ROOT + "/group/green-site/")
    why = None
    if OVERRIDE.search(cmd) and not SANCTIONED.search(cmd):
        why = "it sets GIVING_RELEASE_BLUE, the release script's own switch"
    elif giving and DEPLOY.search(cmd) and "--dry-run" not in cmd and not SANCTIONED.search(cmd):
        why = "it deploys giving directly"
    elif LIVE_DB.search(cmd) and re.search(r"consensor-giving(?!-green)", cmd):
        why = "it runs a remote command on giving's live database"
    msg = user_msg = None
    if not why:
        others = sorted(ready_targets(cmd) - {agent})
        if READY_FOR.search(cmd) and WHO_ENV.search(cmd):
            msg = ("Blocked: this command changes the marks that say which agent is running live-log.py (CLAUDECODE, "
                   "CURSOR_AGENT, env -i/-u). Mark only your own work ready, from your own shell as it is.")
        elif others:
            msg = ready_refusal(others[0], agent)
        if not msg:
            return out({"permission": "allow"}) if agent == "cursor" else None
        user_msg = f"Blocked {agent} from marking another agent's giving work ready."
    msg = msg or (f"Blocked: {why}. giving goes live only through release-blue.command (project root), which first checks that "
           "no other agent has unfinished work (group/LIVE.md), builds, runs the tests, records a rollback point and updates green. "
           f"Mark your own work finished with: python3 -I {ROOT}/group/live/live-log.py ready {agent} \"what\", "
           f"then release with: {ROOT}/release-blue.command {agent}   (only when ōkina has said to release).")
    if agent == "cursor":
        out({"permission": "deny", "agent_message": msg,
             "user_message": user_msg or "Blocked a direct deploy of giving. Releases go through release-blue.command."})
    else:
        out({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": msg}})


def selftest():
    """Runs pending() and record() against a scratch log (never group/LIVE.md). Exit 1 if any case is wrong."""
    import tempfile
    global LOG
    t0 = time.time() - 3600
    stamp = lambda k: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t0 + k))
    released = "cursor·cli | released | 84a3c7a1-2ed5-4935-a38e-7c5ca736efb7 (blue-20261014T234516Z)"
    # (what it shows, log lines after a release, who releases, agents the check must name)
    cases = [
        ("15 Oct 09:45:44: Cursor's ready-and-release line, logged after its own release", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Mapping page scrolls with the document\" && ./rel"], "claude", set()),
        ("15 Oct 10:12:47: the same, cut inside the ready message", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && node --check publish/giving/static/room.js && python3 -I group/live/live-log.py ready cursor \"Ro"], "claude", set()),
        ("15 Oct 06:53:55: the same, cut at ./r", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Mapping page: space cube, self-contained\" && ./r"], "claude", set()),
        ("a cut old line ending in a bare r (could be rm)", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Mapping page: space cube, self-contained\" && r"], "claude", {"cursor"}),
        ("a real edit after the release", ["cursor·333b | edit | publish/giving/src/index.js"], "claude", {"cursor"}),
        ("a shell heredoc writing src/index.js", [
            "cursor·333b | shell | (shell) cd ~/Desktop/consensorAI/design-systems-09Oct26/publish/giving; python3 -I - <<'PYEND' p=\"src/index.js\"; s=open(p).read() a=''' const tries"], "claude", {"cursor"}),
        ("the same heredoc by Claude, Cursor releasing", [
            "claude·eb6c | shell | (shell) cd ~/Desktop/consensorAI/design-systems-09Oct26/publish/giving; python3 -I - <<'PYEND' p=\"src/index.js\"; s=open(p).read() a=''' const tries"], "cursor", {"claude"}),
        ("sed -i on static/room.js", ["cursor·333b | shell | (shell) sed -i '' 's/a/b/' publish/giving/static/room.js"], "claude", {"cursor"}),
        ("cp into the giving source", ["cursor·333b | shell | (shell) cp ~/Downloads/room.js publish/giving/static/room.js"], "claude", {"cursor"}),
        ("echo into a file", ["cursor·333b | shell | (shell) echo hi > publish/giving/src/index.js"], "claude", {"cursor"}),
        ("a write after the release in the same line", [
            "cursor·333b | shell | (shell) ./release-blue.command cursor && sed -i '' s/a/b/ publish/giving/src/index.js"], "claude", {"cursor"}),
        ("running build.py (not on the harmless list)", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && python3 -I publish/giving/build.py && ls -lh publish/giving/public/maps"], "claude", {"cursor"}),
        ("a command inside $(…)", ["cursor·333b | shell | (shell) echo $(sed -i '' s/a/b/ publish/giving/src/index.js)"], "claude", {"cursor"}),
        ("an old line that joined two lines: ls … rm …", ["cursor·333b | shell | (shell) ls publish/giving/src rm publish/giving/src/old.js"], "claude", {"cursor"}),
        ("a cut old line with a cp before the cut", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && cp /tmp/a.js publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Ro"], "claude", {"cursor"}),
        ("a new cut line ending in … (the hook saw it all and said shell)", [
            "cursor·333b | shell | (shell) node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Mapping page scrolls with the document\" && ./rel…"], "claude", {"cursor"}),
        ("reading only: grep, head, sed -n", [
            "claude·955e | shell | (shell) grep -n foo publish/giving/src/index.js | head -5; sed -n 1,20p publish/giving/BUILD.md"], "cursor", set()),
        ("a run line", ["cursor·333b | run | (shell) node --check publish/giving/src/index.js && ./release-blue.command cursor"], "claude", set()),
        ("an edit, then that agent's ready", ["cursor·333b | edit | publish/giving/src/index.js", "cursor·cli | ready | done"], "claude", set()),
        ("the releaser's own edit", ["claude·955e | edit | publish/giving/src/index.js"], "claude", set()),
        ("an edit outside the giving source", ["cursor·333b | edit | group/work/mapping/pages/x.html"], "claude", set()),
    ]
    # (command as the hook sees it, what record() must log it as)
    records = [
        ("node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready cursor \"Mapping page scrolls with the document\" && ./release-blue.command cursor", "run"),
        ("cat publish/giving/BUILD.md | head -120; echo '-----'; cat release-blue.command; echo '-----'; sed -n 55,75p group/work/speed/HANDOFF.md", "run"),
        ("cd publish/giving && python3 -I - <<'PY'\np = 'src/index.js'; s = open(p).read()\nopen(p, 'w').write(s)\nPY", "shell"),
        ("ls publish/giving/src\nrm publish/giving/src/old.js", "shell"),
        ("cat publish/giving/src/index.js > publish/giving/static/copy.js", "shell"),
    ]
    real, fails, n = LOG, [], 0
    with tempfile.TemporaryDirectory() as d:
        LOG = os.path.join(d, "LIVE.md")
        try:
            for name, body, releaser, want in cases:
                with open(LOG, "w", encoding="utf-8") as f:
                    f.write(HEADER + f"{stamp(0)} | {released}\n" + "".join(f"{stamp(k + 1)} | {l}\n" for k, l in enumerate(body)))
                got, n = set(pending(releaser)), n + 1
                print(("ok  " if got == want else "FAIL") + f"  {name}: " + (", ".join(sorted(got)) + " flagged" if got else "passes"))
                if got != want:
                    fails.append(name)
            with open(LOG, "w", encoding="utf-8") as f:
                f.write(HEADER + f"{stamp(0)} | {released}\n")
            for cmd, want in records:
                record({"tool_name": "Bash", "tool_input": {"command": cmd}, "session_id": "self"}, "cursor")
                got, n = (parse(lines()[-1]) or (0, "", "", ""))[2], n + 1
                print(("ok  " if got == want else "FAIL") + f"  hook logs {cmd.splitlines()[0][:70]!r} as {got or 'nothing'}")
                if got != want:
                    fails.append(cmd)
            shown = (parse(lines()[1]) or (0, "", "", ""))[3]
            n += 1
            if not (shown.endswith("…") and len(shown) == len("(shell) ") + SHELL_SHOWN + 1):
                fails.append("cut marker")
            print(("ok  " if "cut marker" not in fails else "FAIL") + "  a long command is cut at 140 characters and ends in …")
            got, n = set(pending("claude")), n + 1
            print(("ok  " if got == {"cursor"} else "FAIL") + "  check over those hook lines names cursor (the heredoc, rm and > lines)")
            if got != {"cursor"}:
                fails.append("check over hook lines")
            # ready: the real command, run the way an agent's shell runs it, against a scratch project folder
            root = os.path.join(d, "root")
            LOG = os.path.join(os.path.realpath(root), "group", "LIVE.md")
            os.makedirs(os.path.dirname(LOG))
            base = {k: v for k, v in os.environ.items() if k not in {m for pair in AGENT_ENV.values() for m in pair}}
            base["LIVE_LOG_ROOT"] = root
            claude_env = {"CLAUDECODE": "1", "CLAUDE_CODE_SESSION_ID": "f217cce2-d1cd-40cd-8bb7-4aecfb6de5c4"}
            cursor_env = {"CURSOR_AGENT": "1", "CURSOR_CONVERSATION_ID": "333b7856-6c28-4a51-ab24-eca2199a1eb3"}
            # (what it shows, the shell's marks, ready for whom, who the new line must name; None = refused, nothing written)
            readies = [
                ("Claude marks its own work", claude_env, "claude", "claude·f217"),
                ("Cursor marks its own work", cursor_env, "cursor", "cursor·333b"),
                ("15 Oct 10:43: Cursor marks Claude's work ready", cursor_env, "claude", None),
                ("Claude marks Cursor's work ready", claude_env, "cursor", None),
                ("ōkina in Terminal marks Claude's work", {}, "claude", "claude·okina"),
                ("ōkina in Terminal marks Cursor's work", {}, "cursor", "cursor·okina"),
                ("a shell with both apps' marks", {**claude_env, **cursor_env}, "claude", None),
            ]
            import subprocess
            for name, marks, target, want in readies:
                with open(LOG, "w", encoding="utf-8") as f:
                    f.write(HEADER + f"{stamp(0)} | {released}\n")
                r = subprocess.run([sys.executable, "-I", os.path.realpath(__file__), "ready", target, "selftest"],
                                   env={**base, **marks}, capture_output=True, text=True)
                last = (parse(lines()[-1]) or (0, "", "", ""))
                got = last[1] if r.returncode == 0 and last[2] == "ready" else None
                ok = got == want and (want is not None or (r.returncode != 0 and "Not marked ready" in r.stderr))
                n += 1
                print(("ok  " if ok else "FAIL") + f"  ready {target}, {name}: " + (f"written as {got}" if got else "refused"))
                if not ok:
                    fails.append(name)
            with open(LOG, "w", encoding="utf-8") as f:  # 10:43 replayed: Claude mid-edit, Cursor's ready claude refused
                f.write(HEADER + f"{stamp(0)} | {released}\n{stamp(1)} | claude·f217 | edit | publish/giving/src/index.js\n")
            subprocess.run([sys.executable, "-I", os.path.realpath(__file__), "ready", "claude", "Owner asked to ship the current tree"],
                           env={**base, **cursor_env}, capture_output=True)
            got, n = set(pending("cursor")), n + 1
            print(("ok  " if got == {"claude"} else "FAIL") + "  10:43 replayed: Cursor's release still stops on Claude's unfinished edit")
            if got != {"claude"}:
                fails.append("10:43 replay")
            # shellguard: the same rule before the command runs, by the hook that knows which app is asking
            import contextlib, io
            ship = 'node --check publish/giving/src/index.js && python3 -I group/live/live-log.py ready {} "Owner asked to ship the current tree" && ./release-blue.command {}'
            guards = [  # (what it shows, command, hook payload extra, forced agent, refused?)
                ("Cursor's 10:43 command", ship.format("claude", "cursor"), {"cursor_version": "2"}, "cursor", True),
                ("the same, through the Claude-style hook Cursor also runs", ship.format("claude", "cursor"), {"cursor_version": "2"}, None, True),
                ("Cursor marking its own", ship.format("cursor", "cursor"), {"cursor_version": "2"}, "cursor", False),
                ("Claude marking its own", ship.format("claude", "claude"), {}, None, False),
                ("Claude marking Cursor's", ship.format("cursor", "claude"), {}, None, True),
                ("Cursor setting CLAUDECODE=1 first", 'CLAUDECODE=1 python3 -I group/live/live-log.py ready claude "x"', {"cursor_version": "2"}, "cursor", True),
                ("Cursor clearing its mark with env -u", 'env -u CURSOR_AGENT python3 -I group/live/live-log.py ready cursor "x"', {"cursor_version": "2"}, "cursor", True),
                ("Claude reading the log for a ready line", 'grep -n "live-log.py ready cursor" group/LIVE.md | tail -3', {}, None, False),
            ]
            for name, cmd, extra, forced, want in guards:
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    shellguard({"tool_name": "Bash", "tool_input": {"command": cmd}, "cwd": ROOT, **extra}, forced)
                got, n = '"deny"' in buf.getvalue(), n + 1
                print(("ok  " if got == want else "FAIL") + f"  shell hook, {name}: " + ("refused" if got else "allowed"))
                if got != want:
                    fails.append(name)
        finally:
            LOG = real
    print(f"selftest: {n - len(fails)} of {n} passed")
    sys.exit(1 if fails else 0)


def cli(mode, args):
    if mode == "ready":
        if len(args) < 1 or args[0] not in ("claude", "cursor"):
            sys.exit("usage: live-log.py ready <claude|cursor> \"what is finished\"")
        agent, me = caller()
        refused = ready_refusal(args[0], agent)
        if refused:
            sys.exit(refused)
        # the line names who marked it: claude·f217 (that session), or claude·okina (a person marked claude's work)
        append(args[0], "ready", " ".join(args[1:])[:200] or "finished and tested", me if agent == args[0] else args[0] + "·okina")
        print(f"marked ready: {args[0]}")
    elif mode == "check":
        releaser = args[0] if args else "okina"
        p = pending(releaser)
        if not p:
            print("no unfinished work from other agents since the last release")
            return
        print("UNFINISHED WORK — not released:")
        for ag, es in p.items():
            files = sorted({e[3] for e in es})
            last = time.strftime("%H:%M", time.localtime(es[-1][0]))
            print(f"  {ag}: {len(es)} change(s), last at {last}, not marked ready")
            for f in files[:12]:
                print(f"     {f}")
        print(f"Each agent marks its work finished with: python3 -I {ROOT}/group/live/live-log.py ready <agent> \"what\"")
        sys.exit(1)
    elif mode == "released":
        append(args[0] if args else "okina", "released", " ".join(args[1:]) or "release")
        print("release recorded")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "selftest":
        return selftest()
    if mode in ("ready", "check", "released"):
        return cli(mode, sys.argv[2:])
    forced = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except Exception:
        payload = {}
    try:
        {"record": record, "inject": inject, "guard": guard, "shellguard": shellguard}[mode](payload, forced)
    except Exception:
        if forced == "cursor" and mode != "record":
            out({"continue": True} if mode == "inject" else {"permission": "allow"})
    if forced == "cursor" and mode == "record":
        out({})


if __name__ == "__main__":
    main()
