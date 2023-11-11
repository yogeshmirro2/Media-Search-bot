import re
import os
class Config(object):
    SESSION = os.environ.get('SESSION', 'Media_search')
    USER_SESSION = os.environ.get('USER_SESSION','User_Bot')
    API_ID = os.environ.get('API_ID')
    API_HASH = os.environ.get('API_HASH')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    BOT_USERNAME = os.environ.get('BOT_USERNAME')
    USERBOT_STRING_SESSION = os.environ.get('USERBOT_STRING_SESSION')
    CACHE_TIME = os.environ.get('CACHE_TIME',300)
    USE_CAPTION_FILTER = os.environ.get('USE_CAPTION_FILTER',True)
    BOT_OWNER = int(os.environ.get("BOT_OWNER"))
    BOT_ADMINS = list(int(x) for x in os.environ.get("BOT_ADMINS","").split())
    BOT_ADMINS.append(BOT_OWNER)
    UPDATES_CHANNEL = os.environ.get('UPDATES_CHANNEL',None)#force subscribe channel id
    INVITE_LINK = os.environ.get("INVITE_LINK",None)#it is invite link of UPDATES_CHANNEL channel
    #DB_CHANNELS = list(int(x) for x in os.environ.get("DB_CHANNELS","").split())
    DATABASE_URL = os.environ.get('DATABASE_URL')#mongodb url
    DATABASE_NAME = os.environ.get('DATABASE_NAME','Media_Search_Bot')
    VERIFY_KEY = os.environ.get("VERIFY_KEY","").split()#multiple VERIFY_KEY separated by space.if VERIFICATION and USE_PRESHORTED_LINK is True then VERIFY_LINK and VERIFY_KEY must be fill.which VERIFY_LINK & VERIFY_KEY related to each other must be same index in both VERIFY_LINK and VERIFY_KEY var like --- "hhjdjdj" this key is ralated to https://www.shorted_link.com then if "hhjdjdj" key is at index 1 then https://www.shorted_link.com must also be at index 1 
    VERIFY_LINK = os.environ.get("VERIFY_LINK","").split()#multiple VERIFY_LINK separated by space.https://t.me/(your bot username without @)?start=verify_(your key which you fill in VERIFY_KEY Var)  ---- this is example of verify link,short this verify link by link shortner and get shorted link this shorted link fill here VERIFY_LINK var.for one verify key one shorted link.verify key and related shorted link must be at same index in their respective var as mention above in VERIFY_KEY
    VERIFICATION = os.environ.get("VERIFICATION",False)
    VERIFY_DAYS = os.environ.get("VERIFY_DAYS",None)
    USE_PRESHORTED_LINK = os.environ.get("USE_PRESHORTED_LINK",False)
    HOW_TO_VERIFY = os.environ.get("HOW_TO_VERIFY","")#if you want give a short instruction to user that how they can complete their VERIFICATION then add here that text
    SHORTNER_API_LINK = os.environ.get("SHORTNER_API_LINK",None)#if VERIFICATION os True and USE_PRESHORTED_LINK is not true then SHORTNER_API and SHORTNER_API_LINK var must be fill
    SHORTNER_API = os.environ.get("SHORTNER_API",None)


