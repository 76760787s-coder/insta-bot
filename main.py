import os
import telebot
import yt_dlp

# Telegram Bot Token
BOT_TOKEN = "8807772730:AAEI5SjejGYhSb_jSADcK_K_2zp2h-gcz3s"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Send me an Instagram Reel or supported video link, and I will download it for you.")

@bot.message_handler(func=lambda message: True)
def download_and_send(message):
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "Please provide a valid video URL.")
        return

    status_msg = bot.reply_to(message, "Downloading video, please wait...")
    
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        bot.edit_message_text("Sending video...", chat_id=message.chat.id, message_id=status_msg.message_id)
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        
        if os.path.exists(filename):
            os.remove(filename)
        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"Error downloading video: {str(e)}", chat_id=message.chat.id, message_id=status_msg.message_id)
        if 'filename' in locals() and os.path.exists(filename):
            os.remove(filename)

print("Bot is running...")
bot.infinity_polling()
