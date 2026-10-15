#!/bin/zsh
# Runs giving's full local tests (dev/e2e.py + dev/crawl.py) against wrangler dev on 8787 and the sign-in stand-in on 8788.
# Uses servers that are already running; otherwise starts them for the run and stops them after. Exit 0 only if both pass.
set -u
G="/Users/okinaasagao/Desktop/consensorAI/design-systems-09Oct26/publish/giving"
W="$HOME/BlueLabs3/projects/consensor-package/node_modules/.bin/wrangler"
up() { [[ "$(curl -s -o /dev/null -w '%{http_code}' "$1")" == "$2" ]]; }
started=()
cleanup() { for p in "${started[@]}"; do kill "$p" 2>/dev/null; done; }
trap cleanup EXIT
cd "$G"
if ! up http://127.0.0.1:8788/ 200 && ! up http://127.0.0.1:8788/ 404; then
  python3 -I dev/consensor-stub.py >/dev/null 2>&1 & started+=($!)
fi
if ! up http://localhost:8787/privacy 200; then
  env -u CLOUDFLARE_API_TOKEN -u GIVING_RELEASE_BLUE "$W" dev --local --ip 127.0.0.1 --port 8787 --local-upstream localhost:8787 \
    --var CONSENSOR_DEV_ORIGIN:http://127.0.0.1:8788 --var ADMIN_EMAILS:stub-mara@test.invalid >/dev/null 2>&1 & started+=($!)
fi
for i in {1..60}; do up http://localhost:8787/privacy 200 && break; sleep 1; done
up http://localhost:8787/privacy 200 || { echo "local site didn't start"; exit 1; }
sleep 1
e2e="$(python3 -I dev/e2e.py 2>&1)"; e=$?
crawl="$(python3 -I dev/crawl.py 2>&1)"; c=$?
print -r -- "$e2e" | grep -E "^FAIL" ; print -r -- "$e2e" | tail -1 | sed 's/^/e2e:   /'
print -r -- "$crawl" | grep -E "^FAIL" ; print -r -- "$crawl" | tail -1 | sed 's/^/crawl: /'
(( e == 0 && c == 0 ))
