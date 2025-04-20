from threading import Lock
import queue

message_queue = queue.Queue()

latest_message = ""
current_ip = ""

'''
    This line creates a thread lock using Python’s threading.Lock() mechanism. 
    It’s a synchronization primitive used to prevent multiple threads 
    from accessing or modifying shared data at the same time, 
    which could lead to inconsistent or corrupted data.
'''
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

def set_ip(ip):
    global current_ip
    with lock:
        current_ip = ip

def get_ip():
    with lock:
        return current_ip