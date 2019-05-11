#!/usr/bin/env python

import telebot
from telebot.types import Message
from telebot import types
import translate


TOKEN = '779969269:AAHV2ttOJ4bcYOfKDdcWty02cfzIh-0__W8'
bot = telebot.TeleBot(TOKEN)
translate_mode = "ru-en"


def make_markup(button_names):
    markup = types.ReplyKeyboardMarkup()
    for it in button_names:
        markup.row(types.KeyboardButton(text=it))
    return markup


menu_button_names = ['Начать изучение новых слов', 'Играть',
                     'Поговорить с ботом', 'Перевести', 'Статистика',
                     'Помощь', 'Настройки']
learn_button_names = ['Изучить слова', 'Изучить идиомы', "В меню"]
play_button_names = ['Выбрать перевод с английского', 'Выбрать перевод с русского', 'В меню']
translate_button_names = ['Перевести с английского на русский', 'Перевести с русского на английский', 'В меню']


menu_markup = make_markup(menu_button_names)
learn_markup = make_markup(learn_button_names)
play_markup = make_markup(play_button_names)
translate_markup = make_markup(translate_button_names)
valid_menu_button_names = ['Начать изучение новых слов', 'Играть', 'Перевести']
options = {
    valid_menu_button_names[0]: learn_markup,
    valid_menu_button_names[1]: play_markup,
    valid_menu_button_names[2]: translate_markup,
}


def choose_from_menu(point):
    @bot.message_handler(func=lambda message: message.text == point)
    def message_handler(message: Message):
        bot.send_message(message.chat.id, "Что делать?", reply_markup=options[point])


def main():
    @bot.message_handler(commands=['menu'])
    @bot.message_handler(func=lambda message: message.text == "В меню")
    def message_handler(message: Message):
        bot.send_message(message.chat.id, "Меню:", reply_markup=menu_markup)

    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda message: message.text == "Помощь")
    def message_handler(message: Message):
        bot.send_message(message.chat.id, "It is a help")

    for it in valid_menu_button_names:
        choose_from_menu(it)

    @bot.message_handler(func=lambda message: message.text == translate_button_names[0])
    def translate_en_ru_handler(message: Message):
        bot.send_message(message.chat.id, "Введите текст (в кавычках):")
        global translate_mode
        translate_mode = "en-ru"

    @bot.message_handler(func=lambda message: message.text == translate_button_names[1])
    def translate_ru_en_handler(message: Message):
        bot.send_message(message.chat.id, "Введите текст (в кавычках):")
        global translate_mode
        translate_mode = "ru-en"

    @bot.message_handler(func=lambda message: message.text[0] == '"' and '"' == message.text[-1])
    def translate_handler(message: Message):
        txt = message.text[1:-1]
        ans = translate.translate(txt, translate_mode)
        bot.send_message(message.chat.id, ans)

    bot.polling()


if __name__ == "__main__":
    main()
