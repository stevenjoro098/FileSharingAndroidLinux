from threading import Lock
import queue

message_queue = queue.Queue()

latest_message = ""

lock = Lock()

def set_message(msg):
    global latest_message
    latest_message = msg

def update_message(msg):
    global latest_message
    with lock:
        latest_message = msg

def get_message():
    with lock:
        return latest_message
