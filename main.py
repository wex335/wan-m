from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses,json



class dd(dict):
    
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__
    

move(0,0)
def chats():
    global converstations
    converstations = s.method("messages.getConversations",{})['items']
    return converstations[0:20]
def getname(id)->str:
    if id>0:
        user = dd(s.userget(id))
        return f"{user.first_name} {user.last_name}"
    if id<0:
        user = dd(s.groupget(id))
        return f"{user.name}"

token = json.loads(open('config.json','r').read(-1))['token']
s= Session(token)

convs = Console(20,40)
messages = Console(90,40)
converstations = []
lp = Lp(s)
chats = chats()



def prmess(message,messconv:curses.window):
    d = messconv.getparyx()
    if(message.from_id==me.id):
        messconv.addstr(f'{message.text}\n')
    elif(message.from_id>0):
        messconv.addstr(getname(message.from_id)+f": {message.text}\n")
    messconv.refresh()


    

wid = 143
hid = 35
me = dd(s.userget())

def printupdate(lst,messconv):
    code = lst[0]
    if code ==4:
        message = dd(s.messget(lst[1]))
        prmess(message,messconv)

def main(conv:curses.window):


    chatconv = curses.newwin(hid,22,1,1)
    chatconv.border()
    bord = curses.newwin(hid,wid-23,1,23)
    bord.border()
    bord.refresh()
    for chat in range(len(chats)):
        chats[chat] = dd(chats[chat])
        if chats[chat].conversation['peer']['id']<2000000000:
            chatconv.addstr(chat+1,1,(getname(chats[chat].conversation['peer']['id']))[:20])
        else: 
            chatconv.addstr(chat+1,1,(chats[chat].conversation['chat_settings']['title'])[:20])
    chatconv.refresh()

    messconv = curses.newwin(hid-4,wid-25,4,24)
    messconv.refresh()
    lp.start(printupdate,messconv)

curses.update_lines_cols()
curses.wrapper(main)