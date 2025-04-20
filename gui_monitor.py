import queue
import tkinter as tk
import qrcode
from PIL import ImageTk

import shared_state

from server.app import message_queue



def generate_qr_image(ip="192.168.0.101", port=5000):
    url = f"http://{ip}:{port}/share"
    qr = qrcode.make(url)
    return ImageTk.PhotoImage(qr)
def listen_for_updates():
    while True:
        try:
            msg = message_queue.get(timeout=1)  # Wait max 1 sec
            print("Tray got message:", msg)
            title = f"LinkBridge | {msg}"
        except queue.Empty:
            continue

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('LinkBridge Monitor')
        self.root.geometry('400x400')

        self.label = tk.Label(root, text='Waiting for data...', font=("Arial",14))

        self.label.pack(expand=True, fill='both', padx=20, pady=20)

        self.update_loop()

        self.qr_img = generate_qr_image()
        self.qr_label = tk.Label(root, image=self.qr_img)
        self.qr_label.pack(pady=10)

    def update_loop(self):
        message = shared_state.get_message()
        self.label.config(text=message if message else "Waiting for data...")
        self.root.after(1000, self.update_loop)

def run_gui():
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
if __name__ == '__main__':
    run_gui()