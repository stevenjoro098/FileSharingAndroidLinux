from threading import Lock

latest_message = ""

lock = Lock()

def update_message(msg):
    global latest_message
    with lock:
        latest_message = msg

def get_message():
    with lock:
        return latest_message
