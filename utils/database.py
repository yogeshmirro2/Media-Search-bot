import re
import types
import logging
import datetime
import secrets
import string
from pyrogram import enums
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import Config

class Database:
    def __init__(self, uri, database_name):
        self._client = AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.mcol = self.db.media_database
        self.fcol = self.db.bot_settings
        
    
    async def new_user(self, id):
        verify_key,verfy_link = await self.verify_key_link_status("get_list")
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat(),
            verify_key=secrets.choice(verify_key) if len(verify_key) != 0 else ''.join(secrets.choice(string.ascii_letters + string.digits)for i in range(7)),
            verify_date=str(datetime.datetime.today()-datetime.timedelta(days=int(Config.VERIFY_DAYS))) if Config.VERIFY_DAYS is not None else str(datetime.datetime.today()-datetime.timedelta(days=2))
        )
    
    async def add_bot_db(self):
        bot_db_dict=dict(
            BOT_DB = "BOT_SETTINGS",
            USE_CAPTION_FILTER=Config.USE_CAPTION_FILTER,
            UPDATES_CHANNEL = Config.UPDATES_CHANNEL,
            INVITE_LINK = Config.INVITE_LINK,
            DB_CHANNELS = [],
            VERIFICATION = Config.VERIFICATION,
            VERIFY_DAYS = Config.VERIFY_DAYS,
            USE_PRESHORTED_LINK = Config.USE_PRESHORTED_LINK,
            VERIFY_KEY = Config.VERIFY_KEY,
            VERIFY_LINK = Config.VERIFY_LINK,
            SHORTNER_API = Config.SHORTNER_API,
            SHORTNER_API_LINK = Config.SHORTNER_API_LINK,
            HOW_TO_VERIFY = Config.HOW_TO_VERIFY,
        )
        await self.fcol.insert_one(bot_db_dict)

    async def check_bot_setting_exist(self):
        bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
        return True if bot_dict else False
    
    async def caption_filter_status(self,update_status_string):
        if (update_status_string=='True' or update_status_string=='False'):
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'USE_CAPTION_FILTER': eval(update_status_string)}})
        else:
            #now return UPDATES_CHANNEL data
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            use_caption_filter = bot_dict.get("USE_CAPTION_FILTER")
            return use_caption_filter
    
    async def update_channel_status(self,update_status_string):
        try:
            channel_status = int(update_status_string)
        except ValueError:
            channel_status = False
        if channel_status:
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'UPDATES_CHANNEL': int(update_status_string)}})
        elif update_status_string=="delete":
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'UPDATES_CHANNEL': None}})
        else:
            #now return UPDATES_CHANNEL data
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            channel_id = bot_dict.get("UPDATES_CHANNEL")
            if update_status_string=="status":
                return True if channel_id is not None else False
            else:
                return channel_id
   
   
    async def update_channel_link_status(self,update_status_string):
        bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
        channel_link = bot_dict.get("INVITE_LINK")
        if ("https" or "t.me") in update_status_string:
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'INVITE_LINK': update_status_string}})
   
        elif update_status_string=="status":
            return True if channel_link is not None else False
        elif update_status_string=="delete":
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'INVITE_LINK': None}})
        
        else:
            return channel_link
    
    
    async def db_channels_status(self,update_status_string):
        bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
        channel_ids_list = bot_dict.get("DB_CHANNELS")
        
        if "delete" in update_status_string:
            channel_id = int(update_status_string.split("_")[-1])
            if channel_id in channel_ids_list:
                channel_ids_list.remove(channel_id)
                await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'DB_CHANNELS': channel_ids_list}})
                return True
            else:
                False
    
        elif "add" in update_status_string:
            channel_id = int(update_status_string.split("_")[-1])
            channel_ids_list.append(channel_id)
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'DB_CHANNELS': channel_ids_list}})
        
        elif update_status_string=="status":
            if len(channel_ids_list)!=0:
                text = f"**CHANNEL_ID       INDEX_FILES**\n"
                for channel in channel_ids_list:
                    count = await self.mcol.count_documents({'channel_id':int(channel)})
                    text+=f"{channel}       {count}\n"
                return text
            else:
                return False
        else:
            return channel_ids_list
        
            
            
    async def verification_status(self,update_status_string):
        if (update_status_string=='True' or update_status_string=='False'):
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFICATION': eval(update_status_string)}})
        else:
            #now return VERIFICATION data
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            verifaction_stats = bot_dict.get("VERIFICATION")
            return verifaction_stats

    async def verify_days_status(self,update_status_string):
        try:
            days_status = int(update_status_string)
        except ValueError:
            days_status = False
        
        if days_status:
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_DAYS': int(days_status)}})
        
        elif update_status_string=='delete':
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_DAYS': None}})
        
        else:
            #return VERIFY_DAYS data
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            verify_day = bot_dict.get("VERIFY_DAYS")
            if update_status_string=="status":
                return True if verify_day is not None else False
            else:
                return verify_day

    async def use_pre_shorted_link_status(self,update_status_string):
        if update_status_string=='True' or update_status_string=='False':
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'USE_PRESHORTED_LINK': eval(update_status_string)}})
        else:
            #return USE_PRESHORTED_LINK Data
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            pre_status = bot_dict.get('USE_PRESHORTED_LINK')
            return pre_status
    
    
    async def verify_key_link_status(self,update_status_string):
        if "|" in update_status_string:
            verify_key_string,verify_link_string= update_status_string.split("|")[0],update_status_string.split("|")[1]
            verify_key_list = verify_key_string.split()
            verify_link_list = verify_link_string.split()
            if len(verify_key_list)!=len(verify_link_list):
                raise Exception("sorry verify_link_list and verify_key_list have not same no. of element") 
            else:
                await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_LINK': verify_link_list}})
                await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_KEY': verify_key_list}})

        elif update_status_string=="delete":
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_LINK': []}})
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'VERIFY_LINK': []}})
        
        else:
            #return VERIFY_KEY and VERIFY_LINK data 
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            verify_key_list = bot_dict.get("VERIFY_KEY")
            verify_link_list = bot_dict.get("VERIFY_LINK")
            if update_status_string=="status":
                return True if len(verify_key_list) & len(verify_link_list)!=0 else False
            else:
                return verify_key_list,verify_link_list
        
        
        
    async def shortner_status(self,update_status_string):
        if "|" in update_status_string:
            api_string,link_string= update_status_string.split("|")[0],update_status_string.split("|")[1]
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'SHORTNER_API': api_string}})
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'SHORTNER_API_LINK': link_string}})
        
        elif update_status_string=="delete":
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'SHORTNER_API': None}})
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'SHORTNER_API_LINK': None}})
        
        
        else:
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            shortner_api = bot_dict.get("SHORTNER_API")
            shortner_api_link = bot_dict.get("SHORTNER_API_LINK")
            if update_status_string=="status":
                return True if shortner_api & shortner_api_link is not None else False
            else:
                return shortner_api,shortner_api_link
    
    
    async def how_to_verify_statua(self,update_status_string):
        if update_status_string=="delete":
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'HOW_TO_VERIFY': ""}})
        
        elif update_status_string=="status":
            bot_dict = await self.fcol.find_one({"BOT_DB":"BOT_SETTINGS"})
            text = bot_dict.get("HOW_TO_VERIFY")
            return text
        else:
            await self.fcol.update_one({"BOT_DB":"BOT_SETTINGS"},{'$set': {'HOW_TO_VERIFY': update_status_string}})
    

    async def get_verify_date(self,id):
        user = await self.col.find_one({'id': int(id)})
        datetime_formate = user.get("verify_date")
        return datetime.datetime.strptime(datetime_formate, '%Y-%m-%d %H:%M:%S.%f')

    async def update_verify_date(self,id):
        user = await self.col.find_one({'id': int(id)})
        day = await self.verify_days_status("get_days")
        await self.col.update_one({'id': id}, {'$set': {'verify_date': str(datetime.datetime.today()+datetime.timedelta(days=int(day)))}})
    
    
    async def update_verify_key(self,id):
        user = await self.col.find_one({'id': int(id)})
        if await self.verify_key_link_status("status"):
            verify_key_list,verify_link_list = await self.verify_key_link_status("get_key_link")
            key = secrets.choice(verify_key_list)
            await self.col.update_one({'id': id}, {'$set': {'verify_key': key}})
        else:
            key = ''.join(secrets.choice(string.ascii_letters + string.digits)for i in range(7))
            await self.col.update_one({'id': id}, {'$set': {'verify_key': key}})



    async def get_verify_key(self,id):
        user = await self.col.find_one({'id': int(id)})
        key = user.get("verify_key")
        if await self.verify_key_link_status("status"):
            verify_key_list,verify_link_list = await self.verify_key_link_status("get_key_link")
            if key not in verify_key_list:
                await self.update_verify_key(id)
                user = await self.col.find_one({'id': int(id)})
                updated_key = user.get("verify_key")
                return updated_key
            else:
                return key
        else:
            return key






    async def add_user(self, id):
        user = await self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        return await self.col.delete_many({'id': int(user_id)})




    async def save_media(self,channel_id:int,file_id:str,file_unique_id:str,file_size:int, file_name:str,file_caption:str):
        media_dict = dict(
            channel_id = channel_id,
            file_id = file_id,
            file_unique_id = file_unique_id,
            file_size = file_size,
            file_name = file_name,
            file_caption = file_caption
        )
        await self.mcol.insert_one(media_dict)

    async def delete_media(self,file_unique_id):
        channel_id = file_unique_id.replace("-","")
        if channel_id.isdigit():
        
            return await self.mcol.delete_many({'channel_id': int(file_unique_id)})
        else:
            return await self.mcol.delete_many({'file_unique_id': file_unique_id})

    async def media_status(self):
        return await self.mcol.count_documents({})
    
    async def get_search_results(self, query, max_results=10, current_page=1):
        query = query.strip()
        if not query:
            raw_pattern = '.'
        elif ' ' not in query:
            raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
        else:
            raw_pattern = query.replace(' ', r'.*[\s\.\+\-_\(\)\[\]]')
    
        try:
            regex = re.compile(raw_pattern, flags=re.IGNORECASE)
        except:
            return [], ''
    
        if await self.caption_filter_status("get_status"):
            filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
        else:
            filter = {'file_name': regex}
        
        total_results = await self.mcol.count_documents(filter)
        if total_results>500:
            total_results=500
        total_pages = total_results//10
        remaining_pages = total_results%10
        if remaining_pages!=0:
            total_pages+=1
            
        cursor = self.mcol.find(filter)
        # Sort by recent
        cursor.sort('$natural', -1)
        
        #try to getting offset
        if current_page==1:
            offset = 0
        
        else:
            if current_page <= total_pages:
                offset = 10*(current_page-1)
        
        # Slice files according to offset and max results
        cursor.skip(offset).limit(max_results)
    
        # Get list of files
        files = await cursor.to_list(length=max_results)
        return files, total_results, total_pages, int(current_page)
    
    
    async def get_file(self,file_unique_id:str):#get file using file_unique_id
        file = await self.mcol.find_one({'file_unique_id': file_unique_id})
        file_id = file.get("file_id")
        file_caption = file.get("file_caption")
        return file_id ,file_caption



db = Database(Config.DATABASE_URL, Config.DATABASE_NAME)
