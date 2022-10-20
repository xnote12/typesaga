import json
from typesaga import TypeSaga

cookies = json.load(open("cookies.json"))
  
bot = TypeSaga()

bot._setAccount(cookies)

bot.play()


