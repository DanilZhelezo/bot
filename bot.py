import logging
import telebot
import yt_dlp
import os
import time

bot = telebot.TeleBot("7787575997:AAGEvAPTR90lv_in3UoW7SxpYcu7M_SVlKI")

class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def init(self):
        super().init(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information["filepath"])
        return [], information

@bot.message_handler(commands=['start'])
def start_cmd(message):
    bot.reply_to(message, "Ky!")

@bot.message_handler(commands=['sea'])
def search(message):
    arg = message.text.split(maxsplit=1)[1]
    bot.reply_to(message, 'Ожидайте...')
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'noplaylist': 'True',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            video = ydl.extract_info(arg, download=True)
        except:
            filename_collector = FilenameCollectorPP()
            ydl.add_post_processor(filename_collector)
            video = ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
            bot.send_document(message.chat.id, open(filename_collector.filenames[0], 'rb'))
            bot.reply_to(message, f'Файл был отправлен!\nСпасибо за использование бота\n\n__{arg}')
            time.sleep(5)
            os.remove(filename_collector.filenames[0])
        else:
            return filename_collector.filenames[0]

if name == "main":
    bot.polling(none_stop=True)