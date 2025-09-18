import discord
from discord.ext import commands
import random
import os
from flask import Flask
import threading

# ------------- Discord Bot ----------------
intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

trigger_words = {
    "เบื่อ": [
        "โอ๊ย เบื่อเหมือนกันเลย 😴",
        "ลองหาอะไรทำไหม จะได้ไม่เบื่อ 😏",
        "เบื่ออะไรกันนักกันหนา 🤪"
    ],
    "หิว": [
        "หิวแล้วหรอ? 🍕🍔",
        "กินไรดีน้า? 🥪",
        "อย่าลืมกินข้าวก่อนหิวตายละ 😝"
    ],
    ".": [
        "จุดทำม่ะอยากโดนดรีมต่อยป่ะ? 👊😆",
        "ระวังหน่อยนะ จุดกำลังสั่น 🤪💨",
        "โอ๊ย จุด! อย่าทำให้โดนต่อย 😂💥"
    ],
    "โง่": [
        "โง่แล้วไง ใครไม่เคยโง่บ้าง 🤣",
        "เฮ้ย อย่าด่าตัวเอง 🤪",
        "โง่หรือเก่ง? เดี๋ยวรู้ 😏"
    ]
}

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    # ตั้งสถานะ Idle + กำลังเล่น
    activity = discord.Game(name="Dream realm 🍄🌙")
    await bot.change_presence(status=discord.Status.idle, activity=activity)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    words_in_message = message.content.lower().split()
    for word in words_in_message:
        if word in trigger_words:
            reply_text = random.choice(trigger_words[word])
            await message.reply(reply_text)
            break

    await bot.process_commands(message)

# ใช้ Environment Variable สำหรับ Token
TOKEN = os.getenv("DISCORD_TOKEN")

# ------------- Flask Healthcheck ------------
app = Flask("")

@app.route("/")
def home():
    return "Bot is running! ✅"

def run_flask():
    app.run(host="0.0.0.0", port=5000)

# ------------- Run Flask + Discord Bot ------------
if __name__ == "__main__":
    # Run Flask ใน Thread แยก เพื่อ Render ping ได้
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
