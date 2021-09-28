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
chstr=""
wid = 143
hid = 35
chwid = 43
me = dd(s.userget())


class Chat:
    def __init__(self, peer, name, advansed):
        self.peer = peer
        self.name = name
        self.adv = advansed

    def __str__(self):
        return f"{self.peer} {self.name} {self.adv}"


def chats():
    res = s.method("messages.getConversations", {})["items"]
    return res[0 : hid - 5]


converstations = []
chats = chats()
for ch in chats:
    pid = ch["conversation"]["peer"]["id"]
    converstations.append(Chat(pid, None, None))
newconv = []
ind = 1


def getname(id) -> str:
    if id > 0:
        user = s.userget(id)
        return f"{user['first_name']} {user['last_name']}"
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
    log(f"\n\n{users} \n\n")
    convus = s.method(
        "users.get", {"user_ids": ",".join(map(str, users)), "fields": "online_info"}
    )
    for uss in convus:
        adv = ""
        if uss["online_info"]["visible"]:
            if uss["online_info"]["is_mobile"]:
                adv += "📳 "
            if uss["online_info"]["is_online"]:
                adv += "Онлайн"
            elif "last_seen" in uss["online_info"]:
                mins = round(
                    (datetime.now().timestamp() - int(uss["online_info"]["last_seen"]))
                    // 60
                )
                if mins > 100:
                    hours = round(mins // 60)
                    if hours > 24:
                        adv += f"{hours/24} дней назад"
                    else:
                        adv += f"{hours} часов назад"
                else:
                    adv += f"{mins} минут назад"
        else:
            adv += "хз, когда онлайн"
        newconv.append(Chat(uss["id"], f"{uss['first_name']} {uss['last_name']}", adv))
    chs = list(filter(lambda ch: ch["conversation"]["peer"]["id"] > 2000000000, chats))
    for chd in chs:
        name = chd["conversation"]["chat_settings"]["title"]
        adv = f"{chd['conversation']['chat_settings']['members_count']} участников"
        ch = Chat(chd["conversation"]["peer"]["id"], name, adv)
        newconv.append(ch)
    log("1234567865rfghjuytrfvgbnil;ukytfguhj" + groups.__str__())
    grups = s.method("groups.getById", {"group_ids": groups, "fields": "online_info"})
    for drr in grups:
        name = drr["name"]
        adv = "Сообщество"
        newconv.append(Chat(-drr["id"], name, adv))


def drawChats(window):
    window.border()
    log(f"DrowChat for {len(newconv)}")
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
    text = message.text
    if (len(message.attachments) > 0) and (message.attachments[0]["type"] == "sticker"):
        text = (
            "Стикер"
            + sticerinfo(message.attachments[0]["sticker"]["sticker_id"]).__str__()
        )
    if message.from_id == me.id:
        messconv.addstr(f"{text}\n")
    elif message.from_id > 0:
        messconv.addstr(getname(message.from_id) + f": {text}\n")
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
        log(f"key {k} {char}")
        if len(char) == 1:
            chstr += char
        elif k == 263 or k == 127:
            log("DELITE")
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
    # try:
    while True:
        k = curs.getch()
        log(k)
        q.put((keydef, k))
        # if k == 6:
        #    changechat(curs)
        # log(f"key {k}")
        # curs.addstr(1,1,k.__str__())
        # curs.refresh


# except Exception as d:
# log(d.with_traceback())
def printupdate(lst, messconv):
    code = lst[0]
    if code == 4:
        message = dd(s.messget(lst[1]))
        if message.peer_id == newconv[ind].peer:
            log(message)
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
    global keydef,tmp,chstr
    while True:
        event = q.get()
        if(event[0] == 'lp'):
            printupdate(event[1],messconv)
        elif(event[0] == 'key'):
            log(f"{event[0]} {event[1]}")
            if event[1] == 6:
                keydef = "keychat"
                tmp = curses.newwin(hid-4, chwid - 3, 2, 2)
                tmp.refresh()
            dokey(event[1])
        elif(event[0] == 'keychat'):
            k = event[1]
            char = str(curses.keyname(k)).split("'")[1]
            if len(char) == 1:
                chstr += char
                tmp.clear()
                tmp.addstr(0, 1, chstr)
                tmp.refresh()
                drowchatsbysearch(chstr)
            elif k == 263 or k == 127:#backspase
                log("DELITE")
                tmp.clear()
                chstr = chstr[:-1]
                tmp.addstr(0, 1, chstr)
                tmp.refresh()
                drowchatsbysearch(chstr)
            if k == 10:#enter
                keydef = "key"
                del tmp
                gotochat(chstr)
                drawChats(c)
            
curses.update_lines_cols()
curses.wrapper(main)
