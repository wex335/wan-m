from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses, json, os, threading
from datetime import datetime
from queue import Queue

q = Queue()
token = json.loads(open("config.json", "r").read(-1))["token"]
s = Session(token)

lp = Lp(s)


class dd(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

keydef = "key"
chardef = "char"
chstr=""
wid = 143
hid = 35
chwid = 43
me = s.userget()


class Chat:
    def __init__(self, peer, name, advansed):
        self.peer = peer
        self.name = name
        self.adv = advansed

    def __str__(self):
        return f"{self.peer} {self.name} {self.adv}"


def chats():
    res = s.method("messages.chats")
    print(res)
    res = res["items"]
    return res[0 : hid - 5]


converstations = []
chats = chats()
for ch in chats:
    pid = ch["id"]
    converstations.append(Chat(pid, None, None))
newconv = []
ind = 0


def getname(id) -> str:
    if id > 0:
        user = s.userget(id)
        return f"{user['name']}"
    if id < 0:
        user = s.groupget(id)
        return f"{user['name']}"


def userinfo():
    users = []
    groups = []
    for c in converstations:
        if c.peer > 0 and c.peer < 2000000000:
            users.append(c.peer)
        elif c.peer < 0:
            groups.append(-c.peer)
    for user in users: 
        uss = s.userget(user)
        newconv.append(Chat(uss["id"], f"{uss['name']}", ""))


def drawChats(window):
    window.border()
    for chat in range(len(newconv)):
        window.addstr(1 + chat, 1, newconv[chat].name[0:chwid-3])
    window.refresh()


def sticerinfo(id):
    fname = f"stickercake//{id}.json"
    if os.path.isfile(fname):
        return json.loads(open(fname, "r").read(-1))["words"]
    else:
        res = s.method("store.getStickersKeywords", {"stickers_ids": id})["dictionary"][
            0
        ]
        open(fname, "w").write(json.dumps({"words": res["words"][0:3]}))
        return sticerinfo(id)


def prmess(message, messconv: curses.window):
    text = message['text']
    if message["from_id"] == me['id']:
        messconv.addstr(f"{text}\n")
    elif message["from_id"] > 0:
        messconv.addstr(getname(message["from_id"]) + f": {text}\n")
    messconv.refresh()


stat = "changechat"
tmp = ()
tmpchs = ()
info = ()

def changechat(win):
    tmp = curses.newwin(hid, chwid - 1, 3, 1)
    stat = "chaangestat"
    k = 0
    while k != 10 and k != 343:
        k = tmp.getch()
        char = curses.keyname(k).__str__().split("'")[1]
        if len(char) == 1:
            chstr += char
        elif k == 263 or k == 127:
            chstr = chstr[:-1]
        tmp.clear()
        tmp.addstr(1, 1, chstr)
        tmp.refresh()
    tmp.clear()
    drawChats(win)
    tmp.refresh()


def dokey(key):
    if key == 6:
        q.put('changechat')


def keyhandler(curs: curses.window):
    while True:
        k = curs.get_wch()
        q.put((keydef, ord(k)))


def charhandler(curs: curses.window):
    while True:
        k = curs.get_wch()
        q.put((chardef, k))



def printupdate(lst, messconv):
    type = lst['type']
    if type in [1,2]:
        message = lst['object']
        if newconv[ind].peer in [message['to_id'],message['from_id']]:
            prmess(message, messconv)


def lpmanager():
    for event in lp.start():
        q.put(("lp", event))

def gotochat(reg):
    chs = list(filter(lambda ch: ch.name.startswith(reg), newconv))
    if len(chs)>0:
        ch = chs[0]
        for g in range(len(newconv)):
            if newconv[g] == ch:
                global ind
                ind = g
                updateinfo()

def drowchatsbysearch(reg):
    chs = list(filter(lambda ch: ch.name.startswith(reg), newconv))
    tmpchs = curses.newwin(hid-8, chwid - 3, 5, 2)
    tmpchs.border()
    for chat in range(len(chs)):
        if(chat == 0):
            tmpchs.addstr(1 + chat, 1, chs[chat].name[0:chwid-5],curses.A_STANDOUT)
        else:
            tmpchs.addstr(1 + chat, 1, chs[chat].name[0:chwid-5])
    tmpchs.refresh()


def updateinfo():
    info.clear()
    info.addstr(newconv[ind].name, curses.A_STANDOUT)
    info.addstr(" " + newconv[ind].adv, curses.A_BOLD)
    info.refresh()


def main(conv: curses.window):
    global info
    info = curses.newwin(1, wid - chwid, 2, chwid + 5)
    userinfo()
    c = curses.newwin(hid, chwid - 1, 1, 1)
    drawChats(c)
    bord = curses.newwin(hid, wid - chwid, 1, chwid)
    bord.border()
    bord.refresh()
    updateinfo()
    messconv = curses.newwin(hid - 4, wid - chwid + 2, 4, chwid + 1)
    messconv.refresh()
    threading.Thread(target=keyhandler, args=[c]).start()
    threading.Thread(target=lpmanager).start()
    global keydef,chardef,tmp,chstr
    while True:
        event = q.get()
        if(event[0] == 'lp'):
            printupdate(event[1],messconv)
        elif(event[0] == 'key'):
            if event[1] == 6:#^F
                keydef = "keychat"
                tmp = curses.newwin(hid-4, chwid - 3, 2, 2)
                tmp.refresh()
                drowchatsbysearch(chstr)
            dokey(event[1])
        elif(event[0] == 'keychat'):
            k = event[1]
            if k == 263 or k == 127:#backspase
                tmp.clear()
                chstr = chstr[:-1]
                tmp.addstr(0, 1, chstr)
                tmp.addstr(0,1,chstr) 
                tmp.refresh()
                drowchatsbysearch(chstr)
            elif k == 10:#enter
                keydef = "key"
                char = "char"
                del tmp
                gotochat(chstr)
                drawChats(c)
            else:
                char = chr(event[1])
                chstr += char
                tmp.clear()
                tmp.addstr(0,1,chstr) 
                tmp.refresh()
                drowchatsbysearch(chstr)
curses.update_lines_cols()
curses.wrapper(main)
