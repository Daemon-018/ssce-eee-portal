#!/data/data/com.termux/files/usr/bin/bash
# EEE Portal launcher — starts Flask at fixed LAN IP:8080 + optional tunnel
# URL: http://<LAN-IP>:8080  (fixed as long as phone stays on same network)

export PATH=$PREFIX/bin:$HOME/bin:$PATH
cd ~/eee_site

# Kill stale instances
pkill -f "python app.py" 2>/dev/null
pkill -f "cloudflared tunnel --url" 2>/dev/null
sleep 1

# Start Flask on fixed port
source .venv/bin/activate
nohup python app.py > server.log 2>&1 &
echo "Flask started on http://0.0.0.0:8080 (PID $!)"

# Wait for readiness
for i in $(seq 1 10); do
  curl -s -o /dev/null -m 2 http://127.0.0.1:8080/ && break
  sleep 1
done

# Print LAN IP (ifconfig works on Termux; ip sometimes empty)
LANIP=$(ifconfig 2>/dev/null | grep -E "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
[ -z "$LANIP" ] && LANIP=$(ip route get 1.1.1.1 2>/dev/null | head -1 | grep -oE 'src [0-9.]+' | awk '{print $2}')
[ -z "$LANIP" ] && LANIP="127.0.0.1"
echo "Fixed URL: http://$LANIP:8080/"
echo "$LANIP" > ~/eee_site/lan_ip.txt

# Optional: start tunnel if requested (backup internet access)
if [ -f ~/eee_site/.tunnel_enabled ]; then
  nohup cloudflared tunnel --url http://127.0.0.1:8080 --protocol http2 --no-autoupdate > cloudflared.log 2>&1 &
  echo "Tunnel starting... URL will appear in cloudflared.log"
fi

echo "Done. Open http://$LANIP:8080/ on any device on the same Wi-Fi."
