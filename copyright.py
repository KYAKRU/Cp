import os
import re
import sys
import time
import datetime
import random
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from pyrogram import filters, Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
import unicodedata
from config import API_ID, API_HASH, BOT_TOKEN, BLACKLIST_FILE, OWNER_ID

def has_special_font(text):
    special_font_regex = re.compile(r'[\u0000-\u001F\u007F-\u009F\u00AD\u0600-\u0605\u061C\u06DD\u070F\u17B4\u17B5\u200B-\u200D\u2028-\u202F\u2060-\u206F\uFEFF\uFFF9-\uFFFB]')
    return bool(special_font_regex.search(text))

API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = BOT_TOKEN
DEVS = [OWNER_ID]

ALL_GROUPS = []
TOTAL_USERS = []
MEDIA_GROUPS = []
DISABLE_CHATS = []
GROUP_MEDIAS = {}
DELETE_MESSAGE = [
    "1 Hour complete, I'm doing my work...",
    "Its time to delete all medias!",
    "No one can Copyright until I'm alive 😤",
    "Hue hue, let's delete media...",
    "I'm here to delete medias 🙋",
    "😮‍💨 Finally I delete medias",
    "Great work done by me 🥲",
    "All media cleared!",
    "hue hue medias deleted by me 😮‍💨",
    "medias....",
    "it's hard to delete all medias 🙄",
]

START_MESSAGE = """
**Hello {}, I'm Anti - CopyRight Bot**

 > **I can save your groups from Copyrights 😉**

 **Work:** I'll Delete all medias of your group in every 1 hour ➰

 **Process?:** Simply add me in your group and promote as admin with delete messages right!
"""

BUTTON = [[InlineKeyboardButton("+ Add me in group +", url="http://t.me/AntiCopyRightRobot?startgroup=s&admin=delete_messages")]]

RiZoeL = Client('RiZoeL-Anti-CopyRight', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
app = Client("sticker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

private_filter = filters.private & filters.command("start")
group_filter = filters.group & filters.command("start")

blacklist_words = set()

with open(BLACKLIST_FILE, "r") as file:
    for line in file:
        blacklist_words.add(line.strip().lower())

delete_mode = True  # Initialize delete_mode
sticker_delete_mode = True  # Initialize sticker_delete_mode
media_delete_mode = True  # Initialize media_delete_mode
pdf_delete_mode = True  # Initialize pdf_delete_mode

async def send_status_message(chat_id, status):
    await RiZoeL.send_message(chat_id, f"Sticker/Media/PDF deletion is now {status}.")

async def enable_sticker_deletion(chat_id):
    if chat_id not in MEDIA_GROUPS:
        MEDIA_GROUPS.append(chat_id)
    await send_status_message(chat_id, "enabled for stickers")

async def disable_sticker_deletion(chat_id):
    if chat_id in MEDIA_GROUPS:
        MEDIA_GROUPS.remove(chat_id)
    await send_status_message(chat_id, "disabled for stickers")

async def enable_media_deletion(chat_id):
    if chat_id not in MEDIA_GROUPS:
        MEDIA_GROUPS.append(chat_id)
    await send_status_message(chat_id, "enabled for media")

async def disable_media_deletion(chat_id):
    if chat_id in MEDIA_GROUPS:
        MEDIA_GROUPS.remove(chat_id)
    await send_status_message(chat_id, "disabled for media")

async def enable_pdf_deletion(chat_id):
    if chat_id not in MEDIA_GROUPS:
        MEDIA_GROUPS.append(chat_id)
    await send_status_message(chat_id, "enabled for PDFs")

async def disable_pdf_deletion(chat_id):
    if chat_id in MEDIA_GROUPS:
        MEDIA_GROUPS.remove(chat_id)
    await send_status_message(chat_id, "disabled for PDFs")

async def delete_media_message(chat_id, message_id):
    try:
        message = await RiZoeL.get_messages(chat_id, message_id)
        if message.text:
            await RiZoeL.delete_messages(chat_id, [message_id], revoke=True)
    except Exception as e:
        print(f"Error deleting media message: {e}")

@RiZoeL.on_message(filters.group & filters.command(["blocktest"]))
async def toggle_sticker_deletion(_, message):
    chat_id = message.chat.id
    global sticker_delete_mode
    sticker_delete_mode = not sticker_delete_mode
    if sticker_delete_mode:
        await enable_sticker_deletion(chat_id)
    else:
        await disable_sticker_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["stickeron"]))
async def enable_sticker_deletion_command(_, message):
    chat_id = message.chat.id
    global sticker_delete_mode
    sticker_delete_mode = True
    await enable_sticker_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["stickeroff"]))
async def disable_sticker_deletion_command(_, message):
    chat_id = message.chat.id
    global sticker_delete_mode
    sticker_delete_mode = False
    await disable_sticker_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["mediaon"]))
async def enable_media_deletion_command(_, message):
    chat_id = message.chat.id
    global media_delete_mode
    media_delete_mode = True
    await enable_media_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["mediaoff"]))
async def disable_media_deletion_command(_, message):
    chat_id = message.chat.id
    global media_delete_mode
    media_delete_mode = False
    await disable_media_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["pdfon"]))
async def enable_pdf_deletion_command(_, message):
    chat_id = message.chat.id
    global pdf_delete_mode
    pdf_delete_mode = True
    await enable_pdf_deletion(chat_id)

@RiZoeL.on_message(filters.group & filters.command(["pdfoff"]))
async def disable_pdf_deletion_command(_, message):
    chat_id = message.chat.id
    global pdf_delete_mode
    pdf_delete_mode = False
    await disable_pdf_deletion(chat_id)

@RiZoeL.on_message(filters.group)
async def delete_blacklisted_messages(client, message):
    try:
        if message.text:
            regular_font_text = unicodedata.normalize('NFKD', message.text)
            if any(word.lower() in regular_font_text.lower() for word in blacklist_words) and delete_mode:
                await message.delete()
            elif has_special_font(message.text) and delete_mode:
                await message.delete()
        elif message.sticker and sticker_delete_mode:
            await delete_media_message(message.chat.id, message.message_id)
        elif (message.video or message.photo or message.animation or message.document) and media_delete_mode:
            await delete_media_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"Error processing message: {e}")

async def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
        return

    for i in MEDIA_GROUPS:
        add_user(i)
        if i in DISABLE_CHATS:
            return
        message_list = GROUP_MEDIAS.get(i)
        if message_list is not None:
            try:
                hue = await RiZoeL.send_message(i, random.choice(DELETE_MESSAGE))
                for msg_id in message_list:
                    msg = await RiZoeL.get_messages(i, msg_id)
                    if msg.sticker is not None and sticker_delete_mode:
                        await delete_media_message(i, msg_id)
                    elif (msg.video or msg.photo or msg.animation or msg.document) and media_delete_mode:
                        await delete_media_message(i, msg_id)
                time.sleep(1)
                await hue.delete()
                GROUP_MEDIAS.pop(i, None)
            except Exception as e:
                print(f"Error: {e}")
            MEDIA_GROUPS.remove(i)
            print("Cleaned all medias ✓")
            print("Waiting for 1 hour")

scheduler = BackgroundScheduler()
scheduler.add_job(AutoDelete, "interval", seconds=1)

scheduler.start()

def starter():
    print('starting bot...')
    RiZoeL.start()
    app.start()
    print('bot Started ✓')
    idle()

if __name__ == "__main__":
    starter()
