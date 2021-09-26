from iop import *
from consoleManager import Console
from lp import *
from internet import *
import curses,json

token = json.loads(open('config.json','r').read(-1))['token']
s= Session(token)
def chats():
    res = s.method("messages.getConversations",{})['items']
    return res[0:35-5]

print(s.userget(1,'online_info'))