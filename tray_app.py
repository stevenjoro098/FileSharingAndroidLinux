import socket
import threading
import time
from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem as item, Menu

from utils import shared_state
from gui_monitor import run_gui
from server.app import app
from utils.shared_state import set_ip, get_ip


# === IP Fetch ===
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return "127.0.0.1"

# === Tray Icon Image ===
def create_image():
    image = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill='green')
    return image

# === Server Start ===
server_running = False
server = 'Start Server'
def start_flask(icon=None, item=None):
    global server_running
    if not server_running:
        threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000), daemon=True).start()
        server_running = True
        print("✅ Flask server started.")
        icon.title = f"ShareBridge | IP: {get_local_ip()} | Running"
    else:
        print("⚠️ Server already running.")

# === Exit App ===
def exit_app(icon, item):
    icon.stop()

def open_gui(icon, item):
    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()

# === Tray Icon ===
icon = pystray.Icon(
    "ShareBridge",
    icon=create_image(),
    title="ShareBridge | IP: (Detecting...)",
    menu=Menu(
        item(server, start_flask),
        item("Show QR", open_gui),
        item("Quit", exit_app)
    )
)

# === IP Monitor ===
def monitor_ip_change():
    current_ip = ""
    while True:
        new_ip = get_local_ip()
        if new_ip != current_ip:
            current_ip = new_ip
            icon.title = f"ShareBridge | IP: {current_ip}"
            set_ip(current_ip)
        msg = shared_state.get_message()
        if msg:
            icon.title = f"ShareBridge | {current_ip}|{msg}"
        time.sleep(5)

# === Run ===
if __name__ == "__main__":
    threading.Thread(target=monitor_ip_change, daemon=True).start()
    icon.run()
