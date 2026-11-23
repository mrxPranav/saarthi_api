#!/bin/sh
# Watches the cloudflared log for the current quick-tunnel URL and publishes it
# to Cloudflare KV (key TUNNEL_URL) whenever it changes.
set -u

LOG=/shared/cloudflared.log
KV_URL="https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/storage/kv/namespaces/${CF_KV_NAMESPACE_ID}/values/TUNNEL_URL"
last=""

apk add --no-cache curl >/dev/null 2>&1 || { echo "Failed to install curl"; exit 1; }

while true; do
  url=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' "$LOG" 2>/dev/null | tail -1)
  if [ -n "$url" ] && [ "$url" != "$last" ]; then
    if curl -fsS -X PUT \
         -H "Authorization: Bearer ${CF_API_TOKEN}" \
         -H "Content-Type: text/plain" \
         --data "$url" "$KV_URL" >/dev/null; then
      echo "Published tunnel URL: $url"
      last="$url"
    else
      echo "Publish failed, will retry"
    fi
  fi
  sleep 15
done
