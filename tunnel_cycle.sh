#!/data/data/com.termux/files/usr/bin/bash
# EEE site Pinggy tunnel auto-restart + Telegram URL notifier
# Kills dead tunnel, starts fresh Pinggy, extracts URL, sends to Telegram.
# Run as a loop: while true; do this; sleep 55m; done

export PATH=$PREFIX/bin:$HOME/bin:$PATH
cd ~/eee_site

# Flask should be up; if not, start it
if ! curl -s -o /dev/null -m 5 http://127.0.0.1:8080/; then
  echo "[$(date)] Flask down, restarting..."
  source .venv/bin/activate
  nohup python app.py > server.log 2>&1 &
  sleep 4
fi

# Kill any old pinggy ssh
pkill -f "free.pinggy.io" 2>/dev/null
sleep 1

# Start fresh Pinggy tunnel (60-min free), capture output
LOG=pinggy.log
: > "$LOG"
ssh -4 -o StrictHostKeyChecking=no -o ServerAliveInterval=30 -o ExitOnForwardFailure=yes \
    -p 443 -R0:localhost:8080 free.pinggy.io > "$LOG" 2>&1 &
TUN_PID=$!

# Wait for URL to appear (up to 30s)
URL=""
for i in $(seq 1 30); do
  URL=$(grep -oE "https://[a-z0-9-]+\.(run\.pinggy-free\.link|free\.pinggy\.net)" "$LOG" 2>/dev/null | head -1)
  [ -n "$URL" ] && break
  sleep 1
done

if [ -z "$URL" ]; then
  echo "[$(date)] TUNNEL FAILED - no URL"
  exit 1
fi

echo "[$(date)] NEW URL: $URL"
echo "$URL" > tunnel_url.txt
echo "$URL" > ~/eee_site/.current_url.txt

# Notify on Telegram
BOT_TOKEN=$(grep -E "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2-)
CHAT_ID=$(grep -E "^TELEGRAM_ALLOWED_USERS=" ~/.hermes/.env | cut -d= -f2- | cut -d, -f1)
if [ -n "$BOT_TOKEN" ] && [ -n "$CHAT_ID" ]; then
  MSG="EEE site new link: $URL"
  curl -s -m 15 "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -d chat_id="$CHAT_ID" -d text="$MSG" >/dev/null 2>&1
  echo "[$(date)] Telegram sent"
fi

echo "[$(date)] tunnel pid $TUN_PID alive, URL valid. Exiting (caller re-loops)."
exit 0
