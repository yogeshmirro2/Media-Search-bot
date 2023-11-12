from base64 import standard_b64encode, standard_b64decode
import time
import string
import datetime
import random
import aiofiles
import asyncio
import traceback
import aiofiles.os
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from utils.database import db
import aiohttp



def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode('ascii')
    return b64


def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode('ascii')
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode('ascii')
    return __str


async def get_file_size(size:int):
    if size is not None:
        if size < 1024:
            file_size = f"[{size} B]"
        elif size < (1024**2):
            file_size = f"[{str(round(size/1024, 2))} KiB] "
        elif size < (1024**3):
            file_size = f"[{str(round(size/(1024**2), 2))} MiB] "
        elif size < (1024**4):
            file_size = f"[{str(round(size/(1024**3), 2))} GiB] "
    else:
        file_size = ""
    return file_size


async def get_diff_min(user_datetime):
    diff_sec = (user_datetime-datetime.datetime.today()).total_seconds()
    diff_min = diff_sec//60
    return diff_min
    
    
    
async def handle_force_sub(bot: Client, cmd: Message):
    updates_channel = await db.update_channel_status("get_id")
    update_channel_link = await db.update_channel_link_status("get_link")
    if (updates_channel and updates_channel_link) is not None:
        
        try:
            user = await bot.get_chat_member(chat_id=updates_channel, user_id=cmd.from_user.id)
            if user.status == "kicked":
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Sorry Sir, You are Banned to use me..",
                    disable_web_page_preview=True
                )
                return 400
        except UserNotParticipant:
            try:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Please Join My Updates Channel to use this Bot!**\n\n"
                         "Due to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=update_channel_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshForceSub")
                            ]
                        ]
                    )
                )
                return 400
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text=f"**🚫Error during Force Subscribe 🚫\nPlz Forward this Error to Bot Owner🛂**\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",
                    disable_web_page_preview=True
                )
                return 400
        except Exception:
            await bot.send_message(
                chat_id=cmd.from_user.id,
                text=f"**🚫Error during Force Subscribe 🚫\nPlz Forward this Error to Bot Owner🛂**\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",
                disable_web_page_preview=True
            )
            return 400
        
    
    else:
        return 200


async def get_shortlink(link):
    if not await db.shortner_status("status"):
        return False
    try:
        API_KEY,API_URL = await db.shortner_status("get_link")
        params = {'api': API_KEY, 'url': link}
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params=params, raise_for_status=True) as response:
                data = await response.json()
                return data["shortenedUrl"]
    except Exception as e:
        print(f"somthing went wrong\nError - {e}\nError Type - {e.__class__.__name__}\nError From :- {__file__,e.__traceback__.tb_lineno}")
        return False
        
        
async def user_verify_status(bot: Client, cmd: Message, edits: Message):
    try:
        key = message.command[1].split("_",1)[1]#getting key from command of verify
        
        if await db.verify_days_status("get_days") is not None and  await db.verification_status("get_status"):
            usr_verify_datetime_formate = await db.get_verify_date(cmd.from_user.id)
            usr_min = await get_diff_min(usr_verify_datetime_formate)
            if usr_min>=0:
                await edits.edit(f"**WTF💀!\nyou are already verified, then why you try for verification again🤒?**")
                return 200 # 200 is sign of move next
            await edits.edit("**Please Wait⚠️ Verifying You...**")
            user_key = await db.get_verify_key(cmd.from_user.id)#getting user verify key from database
            day = await db.verify_days_status("get_days")
            if key==user_key:
                await db.update_verify_date(cmd.from_user.id)
                await db.update_verify_key(cmd.from_user.id)
                await edits.edit(f"**__Verification Complete ️☑️__\nyour verification valid till next__ {day}__ days")
                return 200
            
            else:
                await edits.edit(f"**This verification link is not for you🚫\nPlease wait... untill generating new verification link for you**")
                await db.update_verify_key(cmd.from_user.id)
                usr_key = await db.get_verify_key(cmd.from_user.id)
                if await db.use_pre_shorted_link_status("status") and await db.verify_key_link_status("status"):
                    verify_key_list,verify_link_list = await db.verify_key_link_status("get_list")
                    how_verify = await db.how_to_verify_statua("status")
                    usr_link = verify_link_list[verify_key_list.index(usr_key)]
                    await edits.edit(f"**your __new verification link__ is👇👇👇👇\n__{usr_link}__\nOnce you verify , your verification valid till next {day} days**\n__--To get any help in Verification Watch Below Tutorial--__\n__{how_verify}__")
                    return 400 #400 is sign of stop furthur step
                elif not await db.use_pre_shorted_link_status("status") and await db.verify_key_link_status("status"):
                    await edits.edit("**use_pre_shorted_link not enable.\nplease report bot owner🙏🙏🙏**")
                    return 400
                elif not await db.verify_key_link_status("status") and await db.use_pre_shorted_link_status("status"):
                    await edits.edit("**there are no verify key or verify link exist.\n please report bot owner🙏🙏🙏**")
                    return 400
                else:
                    usr_link_short = f"https://telegram.me/{Config.BOT_USERNAME}?start=verify_{usr_key}"
                    shorted_link = await get_shortlink(usr_link_short)
                    if shorted_link:
                        how_verify = await db.how_to_verify_statua("status")
                        await edits.edit(f"**your new verification link is👇👇👇👇\n{shorted_link}\nOnce you verify , your verification valid till next {day} days\n__--To get any help in Verification Watch Below Tutorial--__\n__{how_verify}__")
                        return 400
                    else:
                        await edits.edit("**there are no shortner availible.\nplease report bot owner🙏🙏🙏")
                        return 400
                    
        elif not await db.verification_status("status"):
            await edits.edit("**Currently verification is off🚫\nyou can use this bot like a free bird**")
            return 200
        
        elif not await db.verify_days_status("status") and await db.verification_status("status"):
            await edits.edit("**verification is enabled but could't find verify days\nplz report bot owner**")
            return 400
    
    
    except Exception as e:
        await edits.edit(f"**there are some problem during verification\n\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`\nplease forward this error to bot owner") 
        return 400
        




async def verify_before_send(bot: Client, cmd: CallbackQuery):
    try:
        if await db.verify_days_status("get_days") is not None and  await db.verification_status("get_status"):
            usr_verify_datetime_formate = await db.get_verify_date(cmd.from_user.id)
            usr_min = await get_diff_min(usr_verify_datetime_formate)
            if usr_min>=0:
                return 20 # 20 is sign of that user is verified
            if await db.use_pre_shorted_link_status("status") and await db.verify_key_link_status("status"):
                day = await db.verify_days_status("get_days")
                await db.update_verify_key(cmd.from_user.id)
                usr_key = await db.get_verify_key(cmd.from_user.id)
                verify_key_list,verify_link_list = await db.verify_key_link_status("get_list")
                how_verify = await db.how_to_verify_statua("status")
                usr_link = verify_link_list[verify_key_list.index(usr_key)]
                btn = [[InlineKeyboardButton("click here to verify",url=usr_link)],[InlineKeyboardButton("Watch Tutorial",url=how_verify)]]
                await cmd.answer("You'll get your file after verification😁😁",show_alert=True)
                await cmd.message.edit(f"**Dear User! You are not verified🚫\nPlease verify now by clicking the link given below😛😛\nYou'll get your file after verification😁😁\nYour verification valid till next `__{day}__`**\n\nप्रिय User! आप verified नहीं हैं, कृपया अभी verify करें।Verify करने के बाद आपको अपनी file मिल जाएगी.\nआपका verification अगले {day} दिन तक मान्य होगा।",reply_markup=btn)
                return 400 #400 is sign of stop furthur step
            elif not await db.use_pre_shorted_link_status("status") and await db.verify_key_link_status("status"):
                await cmd.message.edit("**use_pre_shorted_link not enable.\nplease report bot owner🙏🙏🙏**")
                return 400
            elif not await db.verify_key_link_status("status") and await db.use_pre_shorted_link_status("status"):
                await cmd.message.edit("**there are no verify key or verify link exist.\n please report bot owner🙏🙏🙏**")
                return 400
            else:
                usr_link_short = f"https://telegram.me/{Config.BOT_USERNAME}?start=verify_{usr_key}"
                shorted_link = await get_shortlink(usr_link_short)
                if shorted_link:
                    how_verify = await db.how_to_verify_statua("status")
                    btn = [[InlineKeyboardButton("click here to verify",url=shorted_link)],[InlineKeyboardButton("Watch Tutorial",url=how_verify)]]
                    await cmd.message.edit(f"**Dear User! You are not verified🚫\nPlease verify now by clicking the link given below😛😛\nYou'll get your file after verification😁😁\nYour verification valid till next `__{day}__`**\n\nप्रिय User! आप verified नहीं हैं, कृपया अभी verify करें।Verify करने के बाद आपको अपनी file मिल जाएगी.\nआपका verification अगले {day} दिन तक मान्य होगा।",reply_markup=btn)
                    return 400
                else:
                    await cmd.message.edit("**there are no shortner availible.\nplease report bot owner🙏🙏🙏")
                    return 400
        elif not await db.verify_days_status("status") and await db.verification_status("status"):
            await cmd.message.edit("**verification is enabled but could't find verify days\nplz report bot owner**")
            return 400
        else:
            return 20
    
    except Exception as e:
        await edits.edit(f"**there are some problem during verification\n\nError - {e}\nError Type - `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`\nplease forward this error to bot owner") 
        return 400



broadcast_ids = {}

async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception as e:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


async def main_broadcast_handler(m, db):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = ''.join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"__Broadcast Started! You will be notified with log file when all the users are notified.__"
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users,
        current=done,
        failed=failed,
        success=success
    )
    async with aiofiles.open('broadcast.txt', 'w') as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user['id']),
                message=broadcast_msg
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user['id'])
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(
                        current=done,
                        failed=failed,
                        success=success
                    )
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    else:
        await m.reply_document(
            document='broadcast.txt',
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed.",
            quote=True
        )
    await aiofiles.os.remove('broadcast.txt')
