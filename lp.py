class Lp:
    def __init__(self, session):
        self.sess = session
        self.lp = session.method(
            "messages.getLongPollServer", {"need_pts": 1, "lp_version": 3}
        )
        self.server = self.lp["server"]
        self.key = self.lp["key"]
        self.ts = self.lp["ts"]

    def start(self):
        while True:
            s = self.sess.ht(
                f"https://{self.server}?act=a_check",
                {"key": self.key, "ts": self.ts, "wait": 25, "mode": 74, "version": 3},
            )
            if "failed" in s:
                if s["failed"] != 1:
                    continue
            self.ts = s["ts"]
            for up in s["updates"]:
                yield up
