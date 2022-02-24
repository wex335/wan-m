import requests, json


def log(text):
    open("a.log", "a").write(f"\n{text}")


class Session:
    def __init__(self, token):
        self.token = token

    def method(self, mname, params: dict = {}):
        params["accesstoken"] = self.token
        response = requests.get(
            f"http://localhost:5000/method/{mname}", params
        )
        log(response.text)
        
        return response.json()

    def userget(self, id: int = None, fields=None):
        return self.method("users.get", {"id": id})

    def messget(self, id: int):
        return self.method("messages.get", {"id": id})

    def ht(self, site, params={}):
        return json.loads(requests.get(f"{site}", params).content.decode("utf-8"))
