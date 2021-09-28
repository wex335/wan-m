from iop import *
from lp import *
from internet import *
import json

print("hello")
token = json.loads(open("config.json", "r").read(-1))["token"]
s = Session(token)
converstations = []


class dd(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Chat:
    def __init__(self, peer, name, advansed):
        self.peer = peer
        self.name = name
        self.adv = advansed


def chats():
    res = s.method("messages.getConversations", {})["items"]
    return res[:]


chats = chats()
print(len(chats))
for chat in range(len(chats)):
    chats[chat] = dd(chats[chat])
    pid = chats[chat].conversation["peer"]["id"]
    print(pid)
    converstations.append(Chat(pid, None, None))

users = []
users.append(1)
for c in converstations:
    if c.peer < 0:
        users.append(-c.peer)
users.append(1)
print(len(users))
print(users)
us = s.method("groups.getById", {"group_ids": users.__str__()})
print(us)
