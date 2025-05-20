import os
from pyrogram import Client, filters
from pyrogram.types import Message
from dotenv import load_dotenv

# पर्यावरण चर लोड करें
load_dotenv()
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# बॉट क्लाइंट बनाएं
app = Client("my_group_manager", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# स्टार्ट कमांड
@app.on_message(filters.command("start") & filters.group)
async def start(client, message: Message):
    await message.reply_text("हाय! मैं आपका ग्रुप मैनेजमेंट बॉट हूँ। /help टाइप करें।")

# हेल्प कमांड
@app.on_message(filters.command("help") & filters.group)
async def help_command(client, message: Message):
    help_text = (
        "मेरे कमांड्स:\n"
        "/start - बॉट शुरू करें\n"
        "/ban - यूजर को बैन करें\n"
        "/welcome - वेलकम मैसेज सेट करें\n"
        "/lock - मैसेज टाइप्स लॉक करें (उदाहरण: /lock sticker url)"
    )
    await message.reply_text(help_text)

# वेलकम मैसेज नए मेंबर्स के लिए
@app.on_message(filters.new_chat_members)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        await message.reply_text(f"स्वागत है, {member.first_name}! कृपया ग्रुप नियम पढ़ें।")

# बैन कमांड (केवल एडमिन्स के लिए)
@app.on_message(filters.command("ban") & filters.group & filters.user(OWNER_ID))
async def ban_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        await client.ban_chat_member(message.chat.id, user_id)
        await message.reply_text("यूजर को बैन कर दिया गया।")
    else:
        await message.reply_text("कृपया उस मैसेज को रिप्लाई करें जिसे बैन करना है।")

# लॉक कमांड (URLs और स्टिकर्स ब्लॉक करें)
@app.on_message(filters.group & (filters.entity("url") | filters.sticker))
async def lock_types(client, message: Message):
    await message.delete()
    await message.reply_text("URLs और स्टिकर्स इस ग्रुप में ब्लॉक हैं।")

# बॉट शुरू करें
print("बॉट शुरू हो रहा है...")
app.run()
