#!/usr/bin/env python

import telebot
from telebot.types import Message, CallbackQuery
from telebot import types
import translate


TOKEN = '779969269:AAHV2ttOJ4bcYOfKDdcWty02cfzIh-0__W8'
bot = telebot.TeleBot(TOKEN)


def make_markup(button_names):
    markup = types.InlineKeyboardMarkup()
    for it in button_names:
        markup.row(types.InlineKeyboardButton(text=it, callback_data=it))
    return markup


menu_button_names = ['Начать изучение новых слов', 'Играть',
                     'Поговорить с ботом', 'Статистика',
                     'Помощь', 'Настройки']
learn_button_names = ['Изучить слова', 'Изучить идиомы', "В меню"]
play_button_names = ['Выбрать перевод с английского', 'Выбрать перевод с русского', 'В меню']


menu_markup = make_markup(menu_button_names)
learn_markup = make_markup(learn_button_names)
play_markup = make_markup(play_button_names)

valid_menu_button_names = ['Начать изучение новых слов', 'Играть']
options = {
    valid_menu_button_names[0]: learn_markup,
    valid_menu_button_names[1]: play_markup,
}


def choose_from_menu(point):
    @bot.callback_query_handler(func=lambda callback: callback.data == point)
    def callback_options_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Что делать?", reply_markup=options[point])



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

    @bot.callback_query_handler(func=lambda callback: callback.data == menu_button_names[0])
    def return_call_back(callback):
        bot.send_message(callback.message.chat.id, "Давай начнем!")

    @bot.callback_query_handler(func=lambda callback: callback.data == "В меню")
    def callback_menu_handler(callback: CallbackQuery):
        print(callback.message.text)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=menu_markup)

    @bot.message_handler(content_types=['text'])
    def translate_handler(message: Message):
        ans = translate.translate(message.text)
        bot.send_message(message.chat.id, ans)

    bot.polling()


if __name__ == "__main__":
    main()
