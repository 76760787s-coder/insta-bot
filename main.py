import os
import telebot
from telebot import apihelper
from yt_dlp import YoutubeDL

apihelper.CONNECT_TIMEOUT = 120
apihelper.READ_TIMEOUT = 120

BOT_TOKEN = "8807772730:AAGw1nuKCzQeWngyyXePd4g4gO6MrKdLpZY"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Send me an Instagram reel or video link, and I will download it for you.")

@bot.message_handler(func=lambda message: True)
def handle_video(message):
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "Please provide a valid URL.")
        return

    msg = bot.reply_to(message, "Downloading video, please wait...")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        bot.edit_message_text("Uploading video, almost done...", message.chat.id, msg.message_id)

        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, timeout=120)

        if os.path.exists(filename):
            os.remove(filename)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")

print("Bot is running...")
bot.infinity_polling(timeout=60, long_polling_timeout=60)
