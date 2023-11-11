import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from info import Config
from utils.database import db

logger = logging.getLogger(__name__)
lock = asyncio.Lock()

@Clients.on_message(filters.private & filters.command('index'))
async def index_files(bot, message):
    """Save channel or group files with the help of user bot"""
    try:
        ch = await db.check_bot_setting_exist()
        if not ch:
            await db.add_bot_db()
        if not Config.USERBOT_STRING_SESSION:
            return await message.reply('Set `USERBOT_STRING_SESSION` in info.py file or in environment variables.')
        elif len(message.command) == 1:
            return await message.reply('Please specify channel id in command.\n\nExample: `/index -10012345678`')
        elif lock.locked():
            return await message.reply('Wait until previous process complete.')
        else:
            msg = await message.reply('Processing...⏳',quote=True)
            chat_id = int(message.text.split('/index ')[-1])
            channel_ids_list = await db.db_channels_status("get_db_list")
            if chat_id not in channel_ids_list:
                await db.db_channels_status(f"add_{chat_id}")
            user_bot = Client('User-bot', Config.API_ID, Config.API_HASH, session_string=Config.USERBOT_STRING_SESSION)
            total_files = 0
    
            async with lock:
                try:
                    async with user_bot:
    
                        async for user_message in user_bot.get_chat_history(chat_id):
                            try:
                                message = await bot.get_messages(chat_id, user_message.id, replies=0)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                message = await bot.get_messages(chat_id, user_message.id, replies=0)
    
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
            
                            
                            else:
                                continue
                            await db.save_media(channel_id,file_id,file_unique_id,file_size,file_name,file_caption)
                            total_files += 1
                            
                
                except ChatWriteForbidden:
                    return await msg.edit("Bot is not an admin in the given channel")
                except PeerIdInvalid:
                    return await msg.edit("Given channel ID is invalid")
                except Exception as e:
                    logger.exception(e)
                    return await msg.edit(f'Error: {e}\n{e.__class__.__name__}\nError From :- `{__file__,e.__traceback__.tb_lineno}`')
                else:
                    return await msg.edit(f'Total {total_files} checked!')
    except Exception as e:
        return await msg.edit(f'Error: {e}\n{e.__class__.__name__}\nError From :- `{__file__,e.__traceback__.tb_lineno}`')import logging
import asyncio

from pyrogram import Client, filters
from pyrogram.errors import FloodWait

from info import USERBOT_STRING_SESSION, API_ID, API_HASH, ADMINS, id_pattern
from utils import save_file

logger = logging.getLogger(__name__)
lock = asyncio.Lock()


@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files with the help of user bot"""

    if not USERBOT_STRING_SESSION:
        await message.reply('Set `USERBOT_STRING_SESSION` in info.py file or in environment variables.')
    elif len(message.command) == 1:
        await message.reply('Please specify channel username or id in command.\n\nExample: `/index -10012345678`')
    elif lock.locked():
        await message.reply('Wait until previous process complete.')
    else:
        msg = await message.reply('Processing...⏳')
        raw_data = message.command[1:]
        user_bot = Client('User-bot', API_ID, API_HASH, session_string=USERBOT_STRING_SESSION)
        chats = [int(chat) if id_pattern.search(chat) else chat for chat in raw_data]
        total_files = 0

        async with lock:
            try:
                async with user_bot:
                    for chat in chats:

                        async for user_message in user_bot.get_chat_history(chat):
                            try:
                                message = await bot.get_messages(chat, user_message.id, replies=0)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                message = await bot.get_messages(chat, user_message.id, replies=0)

                            for file_type in ("document", "video", "audio"):
                                media = getattr(message, file_type, None)
                                if media is not None:
                                    break
                            else:
                                continue
                            media.file_type = file_type
                            media.caption = message.caption
                            await save_file(media)
                            total_files += 1
            except Exception as e:
                logger.exception(e)
                await msg.edit(f'Error: {e}')
            else:
                await msg.edit(f'Total {total_files} checked!')
