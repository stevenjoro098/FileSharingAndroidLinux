import queue
import tkinter as tk
import qrcode
from PIL import ImageTk

from utils import shared_state
from server.app import message_queue
from utils.shared_state import get_ip


def generate_qr_image(ip, port=5000, size=(300, 300)):
    """
    Generates a QR code for the provided IP and port.
    Returns a PhotoImage compatible with Tkinter.
    """
    url = f"http://{ip}:{port}/share"
    qr = qrcode.make(url)
    qr = qr.resize(size)
    return ImageTk.PhotoImage(qr)

def listen_for_updates():
    """
    Optional background thread to listen for new messages via queue.
    (Currently not used directly in the GUI but useful if you want to update tray, etc.)
    """
    while True:
        try:
            msg = message_queue.get(timeout=1)
            print("Tray got message:", msg)
            title = f"ShareBridge | {msg}"
        except queue.Empty:
            continue

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('ShareBridge Monitor')
        self.root.geometry('300x400')

        # Display message label
        self.label = tk.Label(root, text='Waiting for data...', font=("Arial", 14))
        self.label.pack(expand=True, fill='both', padx=10, pady=10)

        # Initialize QR code
        self.last_ip = get_ip() or '127.0.0.1'
        self.qr_img = generate_qr_image(self.last_ip)
        self.qr_label = tk.Label(root, image=self.qr_img)
        self.qr_label.pack(pady=10)

        # Start the UI update loop
        self.update_loop()

    def update_loop(self):
        # Update text message
        message = shared_state.get_message()
        self.label.config(text=message if message else "Waiting for data...")

        # Check and update QR if IP has changed
        current_ip = get_ip()
        if current_ip != self.last_ip:
            self.last_ip = current_ip or '127.0.0.1'
            self.qr_img = generate_qr_image(self.last_ip)
            self.qr_label.configure(image=self.qr_img)
            self.qr_label.image = self.qr_img  # Prevent garbage collection

        self.root.after(1000, self.update_loop)

def run_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()

if __name__ == '__main__':
    run_gui()
