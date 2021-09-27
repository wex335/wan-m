from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses,json,os,threading
from datetime import datetime



token = json.loads(open('config.json','r').read(-1))['token']
s= Session(token)

convs = Console(20,40)
messages = Console(90,40)
converstations = []
lp = Lp(s)

class dd(dict):
    
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    

wid = 143
hid = 35
chwid = 43
me = dd(s.userget())
class Chat():
    def __init__(self,peer,name,advansed):
        self.peer=peer
        self.name = name
        self.adv = advansed

def chats():
    res = s.method("messages.getConversations",{})['items']
    return res[0:hid-5]

converstations = []
ind = 5
chats = chats()
def getname(id)->str:
    if id>0:
        user = s.userget(id)
        return f"{user['first_name']} {user['last_name']}"
    if id<0:
        user = s.groupget(id)
        return f"{user['name']}"

def sticerinfo(id):
    fname = f'stickercake//{id}.json'
    if(os.path.isfile(fname)):
        return json.loads(open(fname,'r').read(-1))['words']
    else:
        res = s.method('store.getStickersKeywords',{'stickers_ids':id})['dictionary'][0]
        open(fname,'w').write(json.dumps({'words':res['words'][0:3]}))
        return sticerinfo(id)

def prmess(message,messconv:curses.window):
    d = messconv.getparyx()
    text = message.text
    if(len(message.attachments)>0) and (message.attachments[0]['type'] == 'sticker'):   
        text = "Стикер"+sticerinfo(message.attachments[0]['sticker']['sticker_id']).__str__()
    if(message.from_id==me.id):
        messconv.addstr(f'{text}\n')
    elif(message.from_id>0):
        messconv.addstr(getname(message.from_id)+f": {text}\n")
    messconv.refresh()
stat = "changechat"
def changechat():
    tmp = curses.newwin(hid,chwid-1,3,1)
    stat = "chaangestat"
    str = ""
    k=0
    while k !=10 or k!=343:
        k = tmp.getch()
        char = curses.keyname(k).__str__().split("'")[1].split("'")[0]
        log(f"key {k} {char}")
        if(len(char)==1):
            str+=char
        elif(k==263 or k == 127):
            log('DELITE')
            str=str[:-1]
        tmp.clear()
        tmp.addstr(1,1,str)
        tmp.refresh()
    tmp.clear()
    tmp.refresh()
def keyhandler(curs:curses.window):
    try:
        while True:
            k = curs.getch()
            if k == 6:
                changechat()
            log(f"key {k}")
            curs.addstr(1,1,k.__str__())
            curs.refresh
    except Exception as d:
        log(d.with_traceback())
def printupdate(lst,messconv):
    code = lst[0]
    if code ==4:
        message = dd(s.messget(lst[1]))
        if(message.peer_id==converstations[ind].peer):
            log(message)
            prmess(message,messconv)


def main(conv:curses.window):

    threading.Thread(target=keyhandler,args=[conv]).start()
    chatconv = curses.newwin(hid,chwid-1,1,1)
    chatconv.border()
    bord = curses.newwin(hid,wid-chwid,1,chwid)
    bord.border()
    bord.refresh()
    for chat in range(len(chats)):
        chats[chat] = dd(chats[chat])
        pid = chats[chat].conversation['peer']['id']
        if pid<2000000000:
            if(pid>0):
                user = dd(s.userget(pid,'online_info'))
                adv = ''
                if(user.online_info['is_mobile']):
                    adv+='📳 '
                if(user.online_info['is_online']):
                    adv+="Онлайн"
                elif('last_seen' in user.online_info):
                    mins = round((datetime.now().timestamp()-int(user.online_info['last_seen']))//60)
                    if(mins>100):
                        hours = round(mins//60)
                        if(hours>24):
                            adv+=f"{hours/24} дней назад"
                        else: adv+=f"{hours} часов назад"
                    else:  adv+=f"{mins} минут назад"
                name = f"{user.first_name} {user.last_name}"
                ch = Chat(pid,name,adv)
                converstations.append(ch)
                chatconv.addstr(chat+1,1,(name[:20]))
            else:   
                name = getname(pid)
                adv = "Сообщество"
                ch = Chat(pid,name,adv)
                converstations.append(ch)
                chatconv.addstr(chat+1,1,(name[:chwid-3]))
        else: 
            name = chats[chat].conversation['chat_settings']['title']
            adv = f"{chats[chat].conversation['chat_settings']['members_count']} участников"
            ch = Chat(pid,name,adv)
            converstations.append(ch)
            chatconv.addstr(chat+1,1,(name)[:chwid-3])
    chatconv.refresh()
    info = curses.newwin(1,wid-chwid,2,chwid+5)
    info.addstr(converstations[ind].name,curses.A_STANDOUT)
    info.addstr(" "+converstations[ind].adv,curses.A_BOLD)
    info.refresh()
    messconv = curses.newwin(hid-4,wid-chwid+2,4,chwid+1)
    messconv.refresh()
    lp.start(printupdate,messconv)

curses.update_lines_cols()
curses.wrapper(main)