import logging
import random

import telebot
from telebot.types import Message
import json
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
logging.basicConfig(level=logging.DEBUG)
try:
    with open("userdata.json", "r", encoding="utf-8") as file:
        user_data = json.load(file)
except FileNotFoundError:
    user_data= {}
@bot.message_handler(commands=["owner"])
def handle_owner(message: Message):
    bot.send_message(message.chat.id,"@almazikhl")
@bot.message_handler(commands=["learn"])
def handle_learn(message: Message):
    if len(message.text.split()) == 1:
        bot.send_message(message.chat.id,"Напишите кол-во слов в формате /learn n, которые вы хотите выучить.")
        return True


    user_words = user_data.get(str(message.chat.id), False)
    if not user_words:
        bot.send_message(message.chat.id, "Слов не существует, добавьте их, используя команду /addword.")
        return True
    try:
        words_number =int(message.text.split()[1])

    except ValueError:
        bot.send_message(message.chat.id,"Введите число после /learn")
    bot.send_message(message.chat.id, "Сейчас начнется обучение. Введите stop для остановки обучения")
    ask_translation(message.chat.id, user_words, words_number)
def ask_translation(chat_id,user_words,words_left):
    if words_left > 0:
        word = random.choice(list(user_words.keys()))
        bot.send_message(chat_id,f"Напиши перевод слова: {word}")
        translation = user_words[word]
        bot.register_next_step_handler_by_chat_id(chat_id,check_translation,translation,words_left)
    else:
        bot.send_message(chat_id,"Урок завершен! Ты молодец!")

def check_translation(message,translation, words_left):
    user_answer = message.text.strip().lower()
    if user_answer == "stop":
        bot.send_message(message.chat.id, "Урок завершен!")
        return True
    if user_answer == translation.lower():
        bot.reply_to(message, "Правильно!")
    else:
        bot.reply_to(message, f"Неправильно! Правельный перевод:{translation}")
    ask_translation(message.chat.id,user_data[str(message.chat.id)],words_left-1)


@bot.message_handler(commands=["addword"])
def handle_addword(message: Message):
    user = user_data.get(str(message.chat.id),{})

    words = message.text.split()[1:]

    if len(words) == 2 and len(words[0])<=15 and len(words[1])<=15:
        user[words[0]] = words[1]
        user_data[str(message.chat.id)] = user
        try:
            with open("userdata.json","w",encoding="utf-8") as file:
                json.dump(user_data,file,ensure_ascii=False, indent=4)
            bot.send_message(message.chat.id, "Слово добавлено.")
        except Exception as e:
            bot.send_message(message.chat.id,f"Слово не добавлено {e}")
    else:
        bot.send_message(message.chat.id, "Слово не добавлено. Использование команды: /addword *слово* *перевод*")
@bot.message_handler(commands=["help"])
def handle_help(message: Message):
    bot.send_message(message.chat.id,"""Это бот для обучения английскому языку
1./learn - Начать обучение
2./owner - Связь с создателем
""")
# @bot.message_handler(func=lambda message: True)
# def handler_Start_Command(message):
#     if message.text.lower() == "кто твой создатель?" :
#         bot.reply_to(message, "@almazikhl")
#     elif message.text.lower() == "когда тебя создали?":
#         bot.reply_to(message, "15.07.2004")
#     elif message.text.lower() == "сколько у тебя комманд?":
#         bot.reply_to(message, "0 комманд")
#     elif message.text.lower() == "гав":
#         bot.reply_to(message, "мяу")
@bot.message_handler(func=lambda message: True)
def handler_all(message: Message):
    bot.reply_to(message,"Я вас не понял. Напишите /help для получения помощи.")
bot.polling()