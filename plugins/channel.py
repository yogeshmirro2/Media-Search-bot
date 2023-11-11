from pyrogram import Client, filters
from utils.database import db

media_filter = filters.document | filters.video | filters.audio


@Client.on_message(filters.channel & media_filter)
async def media(bot, message):
    """Media Handler"""
    try:
        if message.chat.id in await db.db_channels_status("get_db_list"):
            if message.video:
                channel_id = int(message.chat.id)
                file_id = message.video.file_id
                file_unique_id = message.video.file_unique_id
                file_size = message.video.file_size
                file_name = message.video.file_name
                file_caption = message.caption if message.caption else ""
            
            elif message.document:
                channel_id = int(message.chat.id)
                file_id = message.document.file_id
                file_unique_id = message.document.file_unique_id
                file_size = message.document.file_size
                file_name = message.document.file_name
                file_caption = message.caption if message.caption else ""
            
            elif message.audio:
                channel_id = int(message.chat.id)
                file_id = message.audio.file_id
                file_unique_id = message.audio.file_unique_id
                file_size = message.audio.file_size
                file_name = message.audio.file_name
                file_caption = message.caption if message.caption else ""
            
            else return
            
            await db.save_media(channel_id,file_id,file_unique_id,file_size,file_name,file_caption)
        
        else:
            await bot.leave_chat(message.chat.id)
            return
    except Exception as e:
        await bot.send_message(Config.BOT_OWNER,f"error during add media to database when media arrive in channel\n{e}\n{e.__class__.__name__}\nError From :- `{__file__,e.__traceback__.tb_lineno}`")
    
