import time
import notify2
notify2.init('News Notifier')
n=notify2.Notification(None)
n.set_urgency(notify2.URGENCY_NORMAL)
n.set_timeout(1000)
n.update('Hello')
n.show()
time.sleep(15)