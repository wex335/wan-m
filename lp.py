import time

def log(text):
    open("a.log", "a").write(f"\n{text}")
class Lp:
    def __init__(self, session):
        self.sess = session
    def start(self):
        while True:
            s = self.sess.method("Pool.get")
            if s['count']>0:
                for up in s["items"]:
                    yield up
                self.sess.method("Pool.read")
            time.sleep(1)
