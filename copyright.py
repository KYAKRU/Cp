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
from pyrogram.enums import ChatMemberStatus, ChatType
from config import API_ID, API_HASH, BOT_TOKEN, BLACKLIST_FILE

API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = BOT_TOKEN
DEVS = [5018319249, 5498943520]

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

@app.on_message(private_filter)
def start_private(_, message: Message):
    message.reply_text("I'm a Sticker Detector Bot! Use me in groups to delete stickers.")

@app.on_message(group_filter)
def start_group(_, message: Message):
    message.reply_text("I'm a Sticker Detector Bot! I will delete stickers in this group.")

@app.on_message(filters.group & filters.sticker)
def delete_stickers_group(_, message: Message):
    message.delete()

@app.on_message(filters.private & filters.sticker)
def delete_stickers_private(_, message: Message):
    message.reply_text("Sticker detected! Use me in groups to delete stickers.")

@RiZoeL.on_message(filters.group & filters.text)
def remove_blacklist_words(_, message: Message):
    chat = message.chat
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if any(word in message.text.lower() for word in blacklist_words):
            message.delete()


@RiZoeL.on_message(filters.command(["stickeron", "stickeron"]))
async def enable_sticker_deletion(_, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if chat.id not in ALL_GROUPS:
            ALL_GROUPS.append(chat.id)
        if chat.id in DISABLE_CHATS:
            DISABLE_CHATS.remove(chat.id)
        if chat.id not in MEDIA_GROUPS:
            MEDIA_GROUPS.append(chat.id)
        await message.reply("Sticker deletion enabled for this group!")

@RiZoeL.on_message(filters.command(["stickeroff", "stickoff"]))
async def disable_sticker_deletion(_, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if chat.id in MEDIA_GROUPS:
            MEDIA_GROUPS.remove(chat.id)
        if chat.id not in DISABLE_CHATS:
            DISABLE_CHATS.append(chat.id)
        await message.reply("Sticker deletion disabled for this group!")

@RiZoeL.on_message(filters.group & filters.text)
def remove_blacklist_words(_, message: Message):
    chat = message.chat
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if any(word in message.text.lower() for word in blacklist_words):
            message.delete()

def add_user(user_id):
    if user_id not in TOTAL_USERS:
        TOTAL_USERS.append(user_id)

@RiZoeL.on_message(filters.command(["ping", "speed"]))
async def ping(_, e: Message):
    start = datetime.datetime.now()
    add_user(e.from_user.id)
    rep = await e.reply_text("**Pong !!**")
    end = datetime.datetime.now()
    ms = (end - start).microseconds / 1000
    await rep.edit_text(f"🤖 **PONG**: `{ms}`ᴍs")

@RiZoeL.on_message(filters.command(["help", "start"]))
async def start_message(_, message: Message):
    add_user(message.from_user.id)
    await message.reply(START_MESSAGE.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(BUTTON))

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["restart", "reboot"]))
async def restart_(_, e: Message):
    await e.reply("**Restarting.....**")
    try:
        await RiZoeL.stop()
    except Exception:
        pass
    args = [sys.executable, "copyright.py"]
    os.execl(sys.executable, *args)
    quit()

@RiZoeL.on_message(filters.user(DEVS) & filters.command(["stat", "stats"]))
async def status(_, message: Message):
    wait = await message.reply("Fetching.....")
    stats = "**Here is total stats of me!** \n\n"
    stats += f"Total Chats: `{len(ALL_GROUPS)}` \n"
    stats += f"Total users: `{len(TOTAL_USERS)}` \n"
    stats += f"Disabled chats: `{len(DISABLE_CHATS)}` \n"
    stats += f"Total Media active chats: `{len(MEDIA_GROUPS)}` \n\n"
    await wait.edit_text(stats)

@RiZoeL.on_message(filters.all & filters.group)
async def watcher(_, message: Message):
    chat = message.chat
    user_id = message.from_user.id
    if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
        if chat.id not in ALL_GROUPS:
            ALL_GROUPS.append(chat.id)
        if chat.id in DISABLE_CHATS:
            return
        if chat.id not in MEDIA_GROUPS:
            if chat.id in DISABLE_CHATS:
                return
            MEDIA_GROUPS.append(chat.id)
        if message.video or message.photo or message.animation or message.document:
            check = GROUP_MEDIAS.get(chat.id)
            if check:
                GROUP_MEDIAS[chat.id].append(message.id)
                print(f"Chat: {chat.title}, message ID: {message.id}")
            else:
                GROUP_MEDIAS[chat.id] = [message.id]
                print(f"Chat: {chat.title}, message ID: {message.id}")

def AutoDelete():
    if len(MEDIA_GROUPS) == 0:
        return

    for i in MEDIA_GROUPS:
        add_user(i)
        if i in DISABLE_CHATS:
            return
        message_list = GROUP_MEDIAS.get(i)
        if message_list is not None:
            try:
                hue = RiZoeL.send_message(i, random.choice(DELETE_MESSAGE))
                
                for msg_id in message_list:
                    msg = RiZoeL.get_messages(i, msg_id)
                    
                    if msg.sticker is not None:
                        RiZoeL.delete_messages(i, [msg_id], revoke=True)
                    elif msg.video or msg.photo or msg.animation or msg.document:
                        RiZoeL.delete_messages(i, [msg_id], revoke=True)
                
                time.sleep(1)
                hue.delete()
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
