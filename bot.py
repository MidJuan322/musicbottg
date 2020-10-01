import telebot
from telebot.types import Message
import os
import datetime
import math
from pytube import YouTube
from pytube import Playlist

bot = telebot.TeleBot('1068994694:AAHIXiT4fmc0WiwumoC-a73TWgbpQYN3mz0')


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


@bot.message_handler(commands=['start'])
def default_commands(message: Message):
    if 'start' in message.text:
        bot.send_message(message.chat.id, 'Добро пожаловать в бота по скачаиванию музыки с Youtube!\n\n'
                                          'Для начала работы'
                                          ' с ботом просто отрпавьте ссылку на видео с Youtube и бот отправит вам '
                                          'аудио с этого видео\n\nУдачного пользования!')


@bot.message_handler(content_types=['text'])
def youtube_download(message):
    try:
        if message.text.startswith('https://www.youtube.com') or ('https://youtu.be/'):
            url = message.text
            title = YouTube(url).title
            bot.send_message(message.chat.id, f'Обрабатываю песню: {title}\n\n'
                                              f'Несколько мгновений и она будет отправлена вам!')
            duration = YouTube(url).length
            if duration < 1800:
                abr_ = YouTube(url).streams.get_audio_only().abr
                dw = YouTube(url).streams.get_audio_only().download()
                statinfo = os.path.getsize(dw)
                bot.send_audio(message.chat.id, audio=open(f'{dw}', 'rb'), title=title,
                               caption=f'\n🎧 {str(datetime.timedelta(seconds=duration))} | {convert_size(statinfo)} | {abr_}',
                               duration=duration)
                os.remove(f'{dw}')
            else:
                bot.send_message(message.chat.id, 'Размер аудио слишком велик\n'
                                                  'Аудиофайл превышает лимит по времени в 30 минут')
    except:
        bot.send_message(message.chat.id, 'Что-то пошло не так')

bot.polling(none_stop=True)