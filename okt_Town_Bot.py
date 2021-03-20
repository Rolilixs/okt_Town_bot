import telebot
from config import *


bot = telebot.TeleBot(TOKEN)

keys = telebot.types.ReplyKeyboardMarkup(True)
keys.row("Помощь", "Информация", "Беседа")

keys_of_admin = telebot.types.ReplyKeyboardMarkup(True, True)
keys_of_admin.row("Принять", "Отклонить")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, message_welcome, reply_markup=keys)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == "помощь":
        bot.send_message(message.chat.id, message_help)
    elif message.text.lower() == "информация":
        bot.send_message(message.chat.id, message_info)
    elif message.text.lower() == "беседа":
        msg = bot.send_message(message.chat.id, "Пожалуйста, напиши свой игровой ник:")
        bot.register_next_step_handler(msg, request_to_admins)
    else:
        bot.send_message(message.chat.id, "Не понимаю, что тут написано\n(О_О)")


def request_to_admins(message):
    global requestUserId
    requestUserId = message.chat.id
    reply_message = "Пользователь с ником \"{}\" хочет вступить в беседу. Принять заявку?".format(message.text)

    for admin_id in ADMINISTRATORS:
        msg = bot.send_message(admin_id, reply_message, reply_markup=keys_of_admin)
        bot.register_next_step_handler(msg, allow_access)


def allow_access(message):
    global requestUserId
    if requestUserId != "":
        if message.text.lower() == "принять":
            bot.send_message(requestUserId, message_invite)
        elif message.text.lower() == "отклонить":
            bot.send_message(requestUserId, "Простите, но мы вам не доверяем\n(-_-)")
    requestUserId = ""


bot.polling(none_stop=True)
