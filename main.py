from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses,json
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
ind = 8
chats = chats()
def getname(id)->str:
    if id>0:
        user = dd(s.userget(id))
        return f"{user.first_name} {user.last_name}"
    if id<0:
        user = dd(s.groupget(id))
        return f"{user.name}"



def prmess(message,messconv:curses.window):
    d = messconv.getparyx()
    if(message.from_id==me.id):
        messconv.addstr(f'{message.text}\n')
    elif(message.from_id>0):
        messconv.addstr(getname(message.from_id)+f": {message.text}\n")
    messconv.refresh()


    

def printupdate(lst,messconv):
    code = lst[0]
    if code ==4:
        message = dd(s.messget(lst[1]))
        if(message.peer_id==converstations[ind].peer):
            prmess(message,messconv)

def main(conv:curses.window):


    chatconv = curses.newwin(hid,22,1,1)
    chatconv.border()
    bord = curses.newwin(hid,wid-23,1,23)
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
                    mins = datetime.now().timestamp()-int(user.online_info['last_seen'])//60
                    if(mins>100):
                        hours = mins//60
                        if(hours>24):
                            adv+=f"{hours//24} дней назад"
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
                chatconv.addstr(chat+1,1,(name[:20]))
        else: 
            name = chats[chat].conversation['chat_settings']['title']
            adv = f"{chats[chat].conversation['chat_settings']['members_count']} участников"
            ch = Chat(pid,name,adv)
            converstations.append(ch)
            chatconv.addstr(chat+1,1,(name)[:20])
    chatconv.refresh()
    info = curses.newwin(1,wid-23,2,25)
    info.addstr(converstations[ind].name,curses.A_STANDOUT)
    info.addstr(" "+converstations[ind].adv,curses.A_BOLD)
    info.refresh()
    messconv = curses.newwin(hid-4,wid-25,4,24)
    messconv.refresh()
    lp.start(printupdate,messconv)

curses.update_lines_cols()
curses.wrapper(main)