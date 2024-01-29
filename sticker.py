from pyrogram import Client, filters
from pyrogram.types import Message

# Define the API key and API hash for your bot
API_ID = 18551731
API_HASH = "227df64ada8de8ebad3b3df5a7603d12"
BOT_TOKEN = "5868706821:AAEiwYP73uQsaB1vHK1eD_pvPKFQqVBRcWo"

app = Client("sticker_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@filters.private & app.on_message(filters.command("start"))
def start_private(_, message: Message):
    message.reply_text("I'm a Sticker Detector Bot! Use me in groups to delete stickers.")

@filters.group & app.on_message(filters.command("start"))
def start_group(_, message: Message):
    message.reply_text("I'm a Sticker Detector Bot! I will delete stickers in this group.")

@filters.group & app.on_message(filters.sticker)
def delete_stickers_group(_, message: Message):
    message.delete()

@filters.private & app.on_message(filters.sticker)
def delete_stickers_private(_, message: Message):
    message.reply_text("Sticker detected! Use me in groups to delete stickers.")

if __name__ == "__main__":
    app.run()
