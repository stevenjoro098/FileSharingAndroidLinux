import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
import subprocess
import sys
import os

def create_image():
    image = Image.new('RGB', (64, 64), color = 'black')
    draw = ImageDraw.Draw(image)
    draw.rectangle((8,8,56,56), fill='green')
    return image

def show_gui():
    subprocess.Popen(['python3','gui_monitor.py'])

# Start the Flask Server
def start_flask():
    subprocess.Popen(['python3', 'app.py'])

# Start Bluetooth server.
def start_bluetooth():
    subprocess.Popen(['python3', 'bluetooth_server.py'])

#Exit the tray

def exit_app(icon, item):
    icon.stop()
    sys.exit()

icon = pystray.Icon('LinkBridge', icon=create_image())
icon.icon = create_image()
icon.menu = pystray.Menu(
    item('Show Monitor', lambda: show_gui()),
    item("Start Flask Server", lambda: start_flask()),
    item("Start Bluetooth Server", lambda: start_bluetooth()),
    item("Quit", exit_app)
)

# Run in a separate thread

def run_tray():
    icon.run()

if __name__ == '__main__':
    threading.Thread(target=run_tray).start()

