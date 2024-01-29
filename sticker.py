from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = 18551731
API_HASH = "227df64ada8de8ebad3b3df5a7603d12"
BOT_TOKEN = "6790998054:AAGJ2sebl3MpWJn7a-MMa8M_HQTydWUuMHY"
app = Client("sticker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

private_filter = filters.private & filters.command("start")
group_filter = filters.group & filters.command("start")

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

if __name__ == "__main__":
    app.run()
