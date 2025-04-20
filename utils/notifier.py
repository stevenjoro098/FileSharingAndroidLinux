import notify2
import os

notify2.init('Link Bridge')

def show_notification(title, message):
    n = notify2.Notification(title, message)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(5000)
    n.show()