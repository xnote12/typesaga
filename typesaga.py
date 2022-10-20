import json, requests as req , os , re , time
from bs4 import BeautifulSoup as bs
from requests import Session
from random import randrange as rand

dash_url = "https://typesaga.com/dashboard"
play_url = "https://typesaga.com/play-to-redeem"
subm_url = "https://typesaga.com/livewire/message/play-to-earn"
    
headers = {
  "User-Agent":"Mozilla/5.0 (Linux; Android 10; POCOPHONE F1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36"
}

class TypeSaga():
  
  def __init__(self):
   
    self.cookie = None
    self.session = None
    self.logged = True
    self.details = None
    self.xcsrf = None
    
    self.banner()
    
  def timer(self,num,remark,typ):
    typ = "%H:%M:%S" if typ == 0 else "%M:%S"
    for x in range(num,0,-1):

      print(f'\x1b[2K\r {remark} : {time.strftime(typ, time.gmtime(x))}', end='')

      time.sleep(1)
    
  def banner(self):
    
    os.system("clear")
    
    print("""  _____             _____             
 |_   _|_ _ ___ ___|   __|___ ___ ___ 
   | | | | | . | -_|__   | .'| . | .'|  By : Xnote12
   |_| |_  |  _|___|_____|__,|_  |__,|
       |___|_|               |___|
 _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
    """)
    
  def _setAccount(self,cookie):
    
    accounts = cookie["remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d"]
    
    for x, act in enumerate(accounts):
      print(f" [{x+1}] Account #{x+1}")
    
    index = int(input(" Choose Account : ") or 0)
  
    self._setCookie({"remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d":accounts[index-1]})
   
  def _setCookie(self,cookie):
    
    self.cookie = cookie
    
  def dashboard(self):
    
    self.banner()
    
    with Session() as s:
      
      fetch_dash = req.get(dash_url,headers=headers,cookies=self.cookie)
      
      content = bs(fetch_dash.content, "html.parser")
      
      p = content.find_all("p", {"class": "text-blue-600 font-medium text-2xl"})
     
      if(len(p) == 0):
        
        self.logged = False
        print("Failed to Login, Invalid Cookie")
      
      else :
        
        name = content.find("input", {"id": "nick1"})["value"]
        
        self.details = [x.text.strip() for x in p]
        
        self.details.append(name)
        
      
  def initData(self):
    
    fetch_play = req.get(play_url,headers=headers,cookies=self.cookie)
    
    content = bs(fetch_play.content, "html.parser")
   
    self.xcsrf = content.find("input", {"name":"_token"})['value']
    
    z = json.loads(content.find('div',attrs={'wire:id':True})["wire:initial-data"])
   
    ck = fetch_play.cookies.get_dict()
    for c in ck:
      self.cookie[c] = ck[c]
    
    fID = z['fingerprint']['id']
    cSum = z['serverMemo']['checksum']
    
    points = rand(35,45)
    factor = points*2
    percent = int((points/45)*100)

    data = json.dumps({"fingerprint":{"id":"1W9fN7G11D9ywJSmecMN","name":"play-to-earn","locale":"en","path":"play-to-redeem","method":"GET","v":"acj"},"serverMemo":{"children":[],"errors":[],"htmlHash":"d59d173a","data":{"points":0},"dataMeta":[],"checksum":"01d0841be0219b9c000f33fc89690d15e47dedb91769f355d6961c4ceb190900"},"updates":[{"type":"fireEvent","payload":{"id":"696","event":"saveResults","params":["1",points,factor,percent,"playtoearn"]}}]})
    
    return data , (points,factor,percent)
    
  
  def play(self):
    
    self.dashboard()
    
    details = self.details
    
    total = 0
  
    if self.logged == True:
      
      energy = int(details[0])
      points = int(details[1])
      name = details[3]
      
      print(f" LOGGED AS : {name} ENERGY : {energy}  CURRENT POINTS : {points}\n")
      
      for x in range(energy,0,-1):
      
        data, score = self.initData()
      
        headers["X-CSRF-TOKEN"] = self.xcsrf
        headers["Content-Type"] = "application/json"
      
        solve = req.post(subm_url,headers=headers,data=data,cookies=self.cookie)
        
        print(f"\x1b[2K\r Energy Left : {x-1} Points : {score[1]} Accuracy : {score[2]}% WPM : {score[0]}")
        
        total += int(score[0])
        
        self.timer(60,"Please wait",1)
        
      else:
        
        print(f"\x1b[2K\r No Energy Left 0/25 Acquired Points : {total}")
        