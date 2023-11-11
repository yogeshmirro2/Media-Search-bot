import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant, QueryIdInvalid
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from utils.database import db
from utils.helpers import get_file_size, verify_before_send

@Client.on_callback_query()
async def button(bot:Client, cmd:CallbackQuery):
    cb_data = cmd.data
    
    if "next" in cb_data:
        unused_var, query, next_page, total_pages = cb_data.split("_")
        if next_page>total_pages:
            next_page = 1
        files, total_results, total_pages, current_page = await db.get_search_results(query, current_page=next_page)
        if len(files)>=1:
            btn = []
            for result in files:
                result_unique_id = result.get('file_unique_id')
                result_caption = result.get("file_caption")
                result_size = result.get("file_size")
                result_size = await get_file_size(result_size)
                btn.append([InlineKeyboardButton(f"{result_size}:{result_caption}", callback_data=f"send_{result_unique_id}")])
            #adding next ,back , close & page No. button
            btn.append([InlineKeyboardButton("BACK",callback_data=f"back_{query}_{current_page-1}_{total_pages}"),InlineKeyboardButton(f"{current_page}/{total_pages}",callback_data="ignore"),InlineKeyboardButton("NEXT",callback_data=f"next_{query}_{current_page+1}_{total_pages}")])
            btn.append([InlineKeyboardButton("Close", callback_data="close")])
            await cmd.mesaage.edit(f"**{total_results}** Result Found for **__{query}__**",reply_markup = btn)
        else:
            return
    
    
    
    elif "back" in cb_data:
        unused_var, query, next_page, total_pages = cb_data.split("_")
        if next_page==0:
            next_page = 1
        files, total_results, total_pages, current_page = await db.get_search_results(query, current_page=next_page)
        if len(files)>=1:
            btn = []
            for result in files:
                result_unique_id = result.get('file_unique_id')
                result_caption = result.get("file_caption")
                result_size = result.get("file_size")
                result_size = await get_file_size(result_size)
                btn.append([InlineKeyboardButton(f"{result_size}:{result_caption}", callback_data=f"send_{result_unique_id}")])
            #adding next ,back , close & page No. button
            btn.append([InlineKeyboardButton("BACK",callback_data=f"back_{query}_{current_page-1}_{total_pages}"),InlineKeyboardButton(f"{current_page}/{total_pages}",callback_data="ignore"),InlineKeyboardButton("NEXT",callback_data=f"next_{query}_{current_page+1}_{total_pages}")])
            btn.append([InlineKeyboardButton("Close", callback_data="close")])
            await cmd.mesaage.edit(f"**{total_results}** Result Found for **__{query}__**",reply_markup = btn)
        else:
            return
    
    
    elif "send" in cb_data:
        response = await verify_before_send(bot,cmd)
        if response == 20:
            file_id , file_caption = await db.get_file(cb_data.split("_")[-1])#cb_data.split("_")[-1] get file_unique_id
            return await bot.send_cached_media(cmd.from_user.id,file_id,file_caption)
        return

    elif "refreshForceSub" in cb_data:
        updates_channel = await db.update_channel_status("get_id")
        update_channel_link = await db.update_channel_link_status("get_link")
        if (updates_channel and updates_channel_link) is not None:
            try:
                user = await bot.get_chat_member(updates_channel, cmd.from_user.id)
                if user.status == "kicked":
                    await cmd.message.edit(
                        text="Sorry Sir, You are Banned to use me. Contact my Support.",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                await cmd.message.edit(
                    text="**You Still Didn't Join ☹️, Please Join My Updates Channel to use this Bot!**\n\n"
                         "Due to Overload, Only Channel Subscribers can use the Bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=update_channel_link)
                            ],
                            [
                                InlineKeyboardButton("🔄 Refresh 🔄", callback_data="refreshmeh")
                            ]
                        ]
                    )
                )
                return
            except Exception:
                await cmd.message.edit(
                    text=f"Something went Wrong. Contact my Support.\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",
                    disable_web_page_preview=True
                )
                return
        await cmd.message.edit(
            text=f"**Hi! I'm Movie/Webserver search bot\nHere you can search movie/webseries name with correct spelling**\nExample :- `/search Avengers`\n\nप्रिय यूजर! मैं एक simple movie/webseries सर्च bot हूं।आप कोई भी movie/webseries सर्च कर सकते है , अगर वह मेरे database में होगी तो आपके भेज दी जाएगी" ,
            
        )
    
    
    elif "verification" in cb_data:
        bool_string = cb_data.rsplit("_",1)[-1]
        try:
            await db.verification_status(bool_string)
        except Exception:
            await cmd.message.edit(
                text=f"Something went Wrong. Contact my Support.\nError⚠️:`{e}`\nError Type➡️ `{e.__class__.__name__}`\nError From :- `{__file__,e.__traceback__.tb_lineno}`",
                disable_web_page_preview=True
            )
            return
        await cmd.message.edit(f"**Now your verification is {bool_string}**")

    elif "use_pre_shorted_link" in cb_data:
        bool_string = cb_data.rsplit("_",1)[-1]
        await db.use_pre_shorted_link_status(bool_string)
        await cmd.message.edit(f"**Now your use_pre_shorted_link is {bool_string}**")

    
    
    
    
    
    
    elif "close" in cb_data:
        await cmd.message.delete(True)
        
        
    try:
        await cmd.answer()
    except QueryIdInvalid: pass
