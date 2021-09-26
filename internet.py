import requests,json

class Session():
    def __init__(self,token,version=5.131):
        self.version = version
        self.token = token

    def method(self,mname,params:dict={}):
        params.setdefault('access_token',[]).append(self.token)
        params.setdefault('v',[]).append(self.version)
        response = requests.get(f"https://api.vk.com/method/{mname}",params).content.decode('utf-8')
        if 'response' in response:
            return json.loads(response)['response']
        return response

    def userget(self,id:int=None,fields=None):
        return self.method('users.get',{'user_ids':id,'fields':fields})[0]

    def groupget(self,id:int=None):
        return self.method('groups.getById',{'group_ids':-id})[0]

    def messget(self,id:int):
        return self.method('messages.getById',{'message_ids':[id]})['items'][0]

    def ht(self,site,params={}):
        return  json.loads(requests.get(f"{site}",params).content.decode('utf-8'))