#!/data/data/com.termux/files/usr/bin/bash
# EEE site: endless Pinggy tunnel supervisor
# Every 50 min: kill old tunnel, start fresh (IPv4), extract URL, notify Telegram.
export PATH=$PREFIX/bin:$HOME/bin:$PATH
cd ~/eee_site

while true; do
  echo "[$(date)] cycle start"
  ./tunnel_cycle.sh
  echo "[$(date)] cycle done, sleeping 50 min"
  sleep 3000   # 50 min
done
