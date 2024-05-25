import os
import logging
import asyncio
from pyrogram import Client,filters,enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup,Message,CallbackQuery
from utils.helpers import get_file_size, handle_force_sub, user_verify_status,verify_before_send, main_broadcast_handler ,str_to_b64 ,b64_to_str
from info import Config
from utils.database import db
logger = logging.getLogger(__name__)
BotCmd = ["start","help","channel","logger","delete_file","delete_channel",
"change_update_channel","delete_update_channel","change_update_channel_link","delete_update_channel_link",
"change_verification","change_verify_days","delete_verify_days","change_use_pre_shorted_link","change_verify_key_link_list",
"delete_verify_key_link_list","change_shortner_api_link","delete_shortner_api_link","change_how_to_verify",
"delete_how_to_verify","status","broadcast","change_use_caption_filter"]


@Client.on_message(filters.text & ~filters.command(BotCmd) & filters.private|filters.group)
async def search(bot, message):
    if message.service:
        return
    if not message.from_user:
        return await message.reply_text("I don't know about you sar :(")
    
    if message.from_user & message.from_user.is_bot:
        return
    
    try:
        user_exist = await db.is_user_exist(message.from_user.id)
        if not user_exist:
            await db.add_user(message.from_user.id)
        
        if message.from_user.id not in Config.BOT_ADMINS:
            back = await handle_force_sub(bot,message)
            if back == 400:
                return
    
    except Exception as e:
        return await message.reply(f"**🚫Error during adding user to Database🚫\nPlz Forward this Error to:- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})🛂**\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`\n\n\
        प्रिय User , नये user को Database में add करने में problem आ रही है । कृपया इस mesaage को  Bot के मालिक :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) को भेज दे" ,quote=True)
    

    try:
        msg = await message.reply("Plz wait⌛ searching your query......\n\nआपकी movie सर्च की जा रही है कृपया प्रतीक्षा⏳ करें......." ,quote=True)
        query = message.text
        files, total_results, total_pages, current_page = await db.get_search_results(query)
        check =""
        if message.chat.type == enums.ChatType.PRIVATE:
            check += "PRIVATE"
        else:
            check += "GROUP"
        if len(files)>=1:
            btn = []
            for result in files:
                result_unique_id = result.get('file_unique_id')
                result_caption = result.get("file_caption")
                result_size = result.get("file_size")
                result_size = await get_file_size(result_size)
                if check == "PRIVATE":
                    btn.append([InlineKeyboardButton(f"{result_size}:{result_caption}" ,callback_data=f"sendp_{result_unique_id}")])
                else:
                    btn.append([InlineKeyboardButton(f"{result_size}:{result_caption}", callback_data=f"sendg_{result_unique_id}")])
            #adding next ,back , close & page No. button
            if total_pages==1:
                btn.append([InlineKeyboardButton(f"{current_page}/{total_pages}",callback_data="ignore")])
            else:
                btn.append([InlineKeyboardButton("BACK",callback_data=f"back_{query}_{current_page-1}_{total_pages}"),InlineKeyboardButton(f"{current_page}/{total_pages}",callback_data="ignore"),InlineKeyboardButton("NEXT",callback_data=f"next_{query}_{current_page+1}_{total_pages}")])
            btn.append([InlineKeyboardButton("Close", callback_data="close")])
            return await msg.edit(f"**{total_results}** Result Found for **__{query}__**",reply_markup = InlineKeyboardMarkup(btn))
        else:
            return await msg.edit(f"**__Can't find any Movie for\n`{query}`\nPlz check your movie name spelling,\
            you can take help of google for correct spelling of movie name__**\nFor any help contact at :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})\n\n\
            प्रिय User आपके द्वारा send की गई मूवी हमारे database में नही है।कृपया भेजी गई मूवी के नाम की spelling check कर ले शायद हो सकता है कि वह spelling गलत हो , \
            spelling चेक करने के लिए आप google की सहायता ले सकते है \nकिसी अन्य सहायता के लिए आप [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) पर सम्पर्क कर कर सकते है",reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('Join Updates Channel', url=f"{Config.INVITE_LINK}")],[InlineKeyboardButton('ADD ME TO YOUR GROUP',url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')]]))
    except Exception as e:
        return await msg.edit(f"**🚫Error during searching files in Database🚫\nPlz Forward this Error to :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})🛂**\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\n\
        Error From :- `{__file__,e.__traceback__.tb_lineno}`\n\nप्रिय User , movie name को Database में सर्च करने में problem आ रही है । कृपया इस mesaage को  Bot के मालिक [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) को भेज दे")



@Client.on_message(filters.command('start') & filters.private|filters.group)
async def start(bot, message):
    """Start command handler"""
    if not message.from_user:
        return await message.reply_text("I don't know about you sar :(")
    
    if message.from_user & message.from_user.is_bot:
        return
    
    if len(message.command)==1:
        try:
            
            user_exist = await db.is_user_exist(message.from_user.id)
            if not user_exist:
                await db.add_user(message.from_user.id)
            
            if message.from_user.id not in Config.BOT_ADMINS:
                back = await handle_force_sub(bot,message)
                if back == 400:
                    return
        
        except Exception as e:
            return await message.reply(f"**🚫Error during adding user to Database🚫\nPlz Forward this Error to :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})🛂**\n\
            Error⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`\n\n\
            प्रिय User , नये user को Database में add करने में problem आ रही है । कृपया इस mesaage को  Bot के मालिक [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) को भेज दे" ,quote=True)
    
       
        return await message.reply(f"**Hi! I'm Movie/Webserver search bot\nHere you can search movie/webseries name with correct spelling\ndirectly send me only movie or webseries name**\nFor any help contact at :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})\n\
        \n\nप्रिय यूजर! मैं एक simple movie/webseries सर्च bot हूं।आप किसी भी movie/webseries को सर्च करने के लिए उस movie या webseries का नाम directly मुझे भेज सकते है, \
        अगर वह मेरे database में होगी तो आपके भेज दी जाएगी \nकिसी सहायता के लिए आप :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) पर सम्पर्क कर सकते है" ,quote=True ,reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('+ADD ME TO YOUR GROUPS', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')],[InlineKeyboardButton('Join Updates Channel', url=f"{Config.INVITE_LINK}")]]))
    
    elif len(message.command)>1 and "verify" in message.command[1]:
        try:
            if message.from_user.id not in Config.BOT_ADMINS:
                edits = await message.reply(f"**Plz __Wait Processing__ Your Verification**")
                response = await user_verify_status(bot,message,edits)
                return
            
            if message.from_user.id in Config.BOT_ADMINS:
                return await message.reply(f"**__You are admin ,then why you are try for verification🤔🤔🤔🤔__**")
        
        
        except Exception as e:
            return await message.reply(f"**__Something Went Wrong in Verification__\nPlz Forward this Error to :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)
    
    elif len(message.command)>1 and "send" in message.command[1]:
        try:
            response = await verify_before_send(bot,message)
            if response == 20:
                file_unique_id = message.command[1].split("_")[-1]
                file_id , file_caption = await db.get_file(file_unique_id)
                return await bot.send_cached_media(message.from_user.id,file_id,file_caption)
            return
        except Exception as e:
            await message.reply(f"somthing went wrong\nplz forward this error to :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})\nError - {e}\nError Type - `{e.__class__.__name__}`\n\
            Error From :- `{__file__,e.__traceback__.tb_lineno}`")
            return
    
    
    
    else:
        return await message.reply(f"**🚫Can't identify your command🚫**")

@Client.on_message(filters.command('help') & filters.private|filters.group)
async def help(bot, message):
    """help command handler"""
    try:
        user_exist = await db.is_user_exist(message.from_user.id)
        if not user_exist:
            await db.add_user(message.from_user.id)
        
        if message.from_user.id not in Config.BOT_ADMINS:
            back = await handle_force_sub(bot,message)
            if back == 400:
                return
    
    except Exception as e:
        return await message.reply(f"**🚫Error during adding user to Database🚫\nPlz Forward this Error to Bot Owner🛂**\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`\n\nप्रिय User , नये user को Database में add करने में problem आ रही है । कृपया इस mesaage को  Bot के मालिक को भेज दे" ,quote=True)

    return await message.reply(f"**Hi! I'm Movie/Webserver search bot\nHere you can send me directly movie/webseries name with correct spelling**\n\
    \n\n if you face any problem, contact at :- [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]})\n\n**प्रिय यूजर! मैं एक simple movie/webseries सर्च bot हूं।आप कोई भी movie/webseries सर्च कर सकते है , \
    अगर वह मेरे database में होगी तो आपके भेज दी जाएगी \nयदि आपको bot को प्रयोग करने में कोई समस्या आ रही ह या bot को कैसे प्रयोग करना है या अन्य किसी सहायता के लिए आप [BOT_ADMIN](tg://user?id={Config.BOT_ADMINS[0]}) पर संपर्क कर सकते है**" ,quote=True ,reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('+ADD ME TO YOUR GROUPS', url=f'http://t.me/{Config.BOT_USERNAME}?startgroup=true')],[InlineKeyboardButton('Join Updates Channel',url=f'{Config.INVITE_LINK}')]]))

@Client.on_message (filters.command('channel') & filters.private & filters.user(Config.BOT_ADMINS))
async def channel_info(bot, message):
    """Send basic information of index channels"""
    try:
        channels_status = await db.db_channels_status("status")
        total_index_files = await db.media_status()
        if channels_status:
            if len(channels_status) < 4096:
                return await message.reply(f"{channels_status}\n\nTotal Index Files : {total_index_files}",quote=True)
            else:
                file = 'Indexed channels.txt'
                with open(file, 'w') as f:
                    f.write(text)
                await message.reply_document(file,quote=True)
                os.remove(file)
                return
        elif total_index_files and not channels_status:
            return await message.reply(f"there are no db_channels but Total Index Files are: `{total_index_files}`",quote=True)
        
        else:
            return await message.reply(f"**__There are no DB_CHANNELS__**",quote=True)
    
    except Exception as e:
        return await message.reply(f"**__something went wrong to get basic information about db_channels__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command('logger') & filters.private & filters.user(Config.BOT_ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        return await message.reply_document('TelegramBot.log')
    except Exception as e:
        return await message.reply(f"**__something went wrong to send log_file__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command('delete_file') & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_file(bot, message):
    """Delete file from database"""
    try:
        reply = message.reply_to_message
        if not (reply and reply.media):
            await message.reply('Reply to file with /delete_file which you want to delete', quote=True)
            return
    
        msg = await message.reply("Processing...⏳", quote=True)
    
        if reply.video:
            file_unique_id = reply.video.file_unique_id
        
        elif reply.document:
            file_unique_id = reply.document.file_unique_id
            
        elif reply.audio:
            file_unique_id = reply.audio.file_unique_id
        
        else:
            await msg.edit('This is not supported file format')
            return
        
        deleted = await db.delete_media(file_unique_id)
        
        if deleted.deleted_count:
            return await msg.edit(f"**Total Files : __`{deleted.deleted_count}`__  are successfully deleted from database**")
        else:
            return await msg.edit('File_id not found in database')
    except Exception as e:
        return await message.reply(f"**__something went wrong during delete file from database__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)
        

@Client.on_message(filters.command('delete_channel') & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_channel(bot, message):
    """Delete Db channel and its index files from database"""
    try:
        if not message.reply_to_message:
            return await message.reply(f'__Reply to channel_id with /delete_channel which you want to delete from database__', quote=True)
        
        reply_text = str(message.reply_to_message.text)
        reply_text1 = reply_text.replace("-","")
        if not reply_text1.isdigit():
            await message.reply(f'__Reply to only channel_id with /delete_channel which you want to delete from database Not a string__', quote=True)
            return
    
        msg = await message.reply("Processing...⏳", quote=True)
        #checking channel_id is in database or not
        db_channels = await db.db_channels_status("get_db_list")
        channel_id = int(reply_text)
        if channel_id in db_channels:
            await msg.edit(f"deleting channel_id from database....")
            await db.db_channels_status(f"delete_{channel_id}")
            await asyncio.sleep(3)
            await msg.edit(f"deleting all index files of this channel from database......")
            count = await db.delete_media(str(channel_id))
            return await msg.edit(f"{channel_id} has been successfully deleted with {count.deleted_count} index files")
        
        else:
            return await msg.edit('channel_id not found in database')
    except Exception as e:
        return await message.reply(f"**__something went wrong during delete file from database__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

@Client.on_message(filters.command('change_update_channel') & filters.private & filters.user(Config.BOT_ADMINS))
async def change_update_channel(bot, message):
    if not message.reply_to_message:
        try:
            update_channel = await db.update_channel_status("get_id")
            return await message.reply(f"**reply any channel id (__Example :- -10023674986__) where bot must be admin\nyour current update_channel_id is __{update_channel}__**")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

    try:
        channel_id = int(message.reply_to_message.text)
    except ValueError:
        return await message.reply(f"**reply only channel id (__Example :- -10023674986__) Not a string**")
    try:
        await db.update_channel_status(channel_id)
        return await message.reply(f"**update_channel_id Successfully changed**")
    except Exception as e:
        return await message.reply(f"**__something went wrong changing update_channel_id__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command('delete_update_channel') & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_update_channel(bot, message):
    try:
        await db.update_channel_status("delete")
        return await message.reply(f"**update_channel_id Successfully deleted**")
    except Exception as e:
        return await message.reply(f"**__something went wrong deleting update_channel_id__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command('change_update_channel_link') & filters.private & filters.user(Config.BOT_ADMINS))
async def change_update_channel_link(bot, message):
    if not message.reply_to_message:
        try:
            update_channel_link = await db.update_channel_link_status("get_link")
            return await message.reply(f"**reply any channel invite link (__Example :- https://t.me/+2K7o4GxMzIx__) where bot must be admin\nyour current update_channel_link is __{update_channel_link}__**")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

    
    channel_invite_link = message.reply_to_message.text
    if not ("https" and "t.me") in channel_invite_link:
        return await message.reply("send update channel_invite_link linke this :- https://t.me/+2K7o4GxMzIx")
    
    
    try:
        await db.update_channel_link_status(channel_invite_link)
        return await message.reply(f"**update_channel invite link Successfully changed**")
    except Exception as e:
        return await message.reply(f"**__something went wrong changing update_channel_id__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command('delete_update_channel_link') & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_update_channel_link(bot, message):
    try:
        await db.update_channel_link_status("delete")
        return await message.reply(f"**update_channel_id Successfully deleted**")
    except Exception as e:
        return await message.reply(f"**__something went wrong deleting update_channel_id__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_verification") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_verification(bot, message):
    try:
        results = await db.verification_status("status")
        if results:
            result = "False"
        else:
            result = "True"
        btn=[[InlineKeyboardButton("click here", callback_data=f"verification_{result}")]]
        return await message.reply(
            text=f"**your current status for verification is --- {str(results)}\n click below to change status👇👇👇",
            reply_markup=InlineKeyboardMarkup(btn),
            quote=True,
            disable_web_page_preview=True
        )

    except Exception as e:
        return await message.reply(f"**__something went wrong__**\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_verify_days") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_verify_days(bot, message):
    if not message.reply_to_message:
        try:
            days = await db.verify_days_status("get_days")
            return await message.reply(f"**reply any intiger Number to add  or change verify_days\n Your current verify_days is {days}**")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

            
    try:
        days = int(message.reply_to_message.text)
        await db.verify_days_status(str(days))
        return await message.reply("**Successfully change verify_days**")
    except ValueError:
        return await message.reply("don't send me text\nsend me only  intiger like --- 6")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("delete_verify_days") & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_verify_days(bot, message):
    try:
        await db.verify_days_status("delete")
        return await message.reply("**Successfully deleted verify_days**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_use_pre_shorted_link") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_use_pre_shorted_link(bot, message):
    try:
        results = await db.use_pre_shorted_link_status("get_status")
        if results:
            result = "False"
        else:
            result = "True"
        btn=[[InlineKeyboardButton("click here", callback_data=f"use_pre_shorted_link_{result}")]]
        return await message.reply(
            text=f"**your current status for use_pre_shorted_link is --- {str(results)}\n click below to change status👇👇👇",
            reply_markup=InlineKeyboardMarkup(btn),
            quote=True,
            disable_web_page_preview=True
        )
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_verify_key_link_list") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_verify_key_link_list(bot, message):
    if not message.reply_to_message:
        try:
            
            list1,list2 = await db.verify_key_link_status("get_list")
            return await message.reply(f"**reply any text which contain verify key and verify link.\nmultiple verify key and verify link separated by space and verify key and verify link must separated by colon(|)\nexample---- key1 key2 key3 key4|link1 link2 link3 link4\nYour current verify key and verify list  is ----\nVerify_Key --- {list1}\nVerify_Link --- {list2} **")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

        
    try:
        await db.verify_key_link_status(message.reply_to_message.text)
        return await message.reply("**Successfully change verify_key_list and verify_link_list**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

@Client.on_message(filters.command("delete_verify_key_link_list") & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_verify_key_link_list(bot, message):
    try:
        await db.verify_key_link_status("delete")
        return await message.reply("**Successfully deleted verify_key and verify_link list**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_shortner_api_link") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_shortner_api_link(bot, message):
    if not message.reply_to_message:
        try:
            api,link = await db.shortner_status("get_shortner")
            return await message.reply(f"**reply any text which contain shortner_api and shortner_api_link.\nshortner_api and shortner_api_link must be separated by colon(|)\nexample---- shortner_api|shortner_api_link\n Your current shortner_api and shortner_api_link  is ----\nShortner_Api --- {api}\nShortner_Api_Link --- {link} **")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)
    try:
        
        await db.shortner_status(message.reply_to_message.text)
        return await message.reply("**Successfully change shortner_api and shortner_api_link**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

@Client.on_message(filters.command("delete_shortner_api_link") & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_shortner_api_link(bot, message):
    try:
        await db.shortner_status("delete")
        return await message.reply("**Successfully deleted shortner_api and shortner_api_link**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("change_how_to_verify") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_how_to_verify(bot, message):
    if not message.reply_to_message:
        try:
            detail = await db.how_to_verify_statua("status")
            return await message.reply(f"**reply any text which you want use as HOW_TO_VERIFY.\nyour current HOW_TO_VERIFY is --- {detail}**")
        except Exception as e:
            return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

        
    try:
        add_detail = message.reply_to_message.text
        await db.how_to_verify_statua(str(add_detail))
        return await message.reply("**Successfully change HOW_TO_VERIFY data**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)

@Client.on_message(filters.command("delete_how_to_verify") & filters.private & filters.user(Config.BOT_ADMINS))
async def delete_how_to_verify(bot, message):
    try:
        await db.how_to_verify_statua("delete")
        return await message.reply("**Successfully deleted HOW_TO_VERIFY data**")
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)


@Client.on_message(filters.command("status") & filters.private & filters.user(Config.BOT_ADMINS))
async def get_total_users(bot, message):
    try:
        count = await db.total_users_count()
        return await message.reply(f"**Total Users in DB:**__{count}__", quote=True)
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)
        
        
@Client.on_message(filters.command("broadcast") & filters.private & filters.user(Config.BOT_ADMINS) & filters.reply)
async def broadcast_handler_open(bot, message):
    await main_broadcast_handler(message, db)


@Client.on_message(filters.command("change_use_caption_filter") & filters.private & filters.user(Config.BOT_ADMINS))
async def change_use_caption_filter(bot, message):
    try:
        results = await db.caption_filter_status("get_status")
        if results:
            result = "False"
        else:
            result = "True"
        btn=[[InlineKeyboardButton("click here", callback_data=f"use_caption_filter_{result}")]]
        return await message.reply(
            text=f"**your current status for use_caption_filter is --- {str(results)}\n click below to change status👇👇👇",
            reply_markup=InlineKeyboardMarkup(btn),
            quote=True,
            disable_web_page_preview=True
        )
    except Exception as e:
        return await message.reply(f"somthing went wrong\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",quote=True)
