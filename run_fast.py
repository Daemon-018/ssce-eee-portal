
from app import app
from waitress import serve
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

local_ip = get_ip()
port = 8080
print(f"🚀 High-Performance Server Starting...")
print(f"🌐 Local Network: http://{local_ip}:{port}/")
print("⚡ Powered by Waitress (Production Grade)")

serve(app, host='0.0.0.0', port=port, threads=8)
