import telebot
from telebot.types import Message, CallbackQuery
from telebot import types
import apiai, json
import translate
import game
import keyboards
import tools
import constants
import config

TOKEN = '779969269:AAHV2ttOJ4bcYOfKDdcWty02cfzIh-0__W8'
bot = telebot.TeleBot(TOKEN)


learn_button_names = ['Изучить слова', 'Изучить идиомы', "В меню"]
play_button_names = ['Выбрать перевод с английского', 'Выбрать перевод с русского', 'В меню']



learn_markup = tools.make_markup(learn_button_names)
play_markup = tools.make_markup(play_button_names)

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
    bot.delete_webhook()
    game_manager = game.GameManager()
    config.is_talking = False

    @bot.callback_query_handler(func=lambda callback: callback.data == "В меню")
    def callback_menu_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)

    @bot.message_handler(commands=['menu'])
    @bot.message_handler(func=lambda message: message.text == "В меню")
    def message_handler(message: Message):
        #bot.edit_message_reply_markup(message_id=message.message_id, chat_id=message.chat.id)
        bot.send_message(message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)
        config.is_talking = False

    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda message: message.text == "Помощь")
    def message_handler(message: Message):
        bot.send_message(message.chat.id, "It is a help")

    @bot.callback_query_handler(func=lambda callback: callback.data in play_button_names)
    def play_handler(callback: CallbackQuery):
        if callback.data == play_button_names[0]:
            game_manager.set_pack(game.family_dict, constants.Languages.EN_RU)
        elif callback.data == play_button_names[1]:
            game_manager.set_pack(game.family_dict, constants.Languages.RU_EN)
        game_manager.is_playing = True
        game_manager.get_guesses(5)
        game_manager.to_guess = next(game_manager.game_guesses)
        answers = game_manager.get_answers(game_manager.to_guess)
        game_manager.send_options(game_manager.to_guess, answers, bot, callback.message.chat.id)

    for it in valid_menu_button_names:
        choose_from_menu(it)



    @bot.callback_query_handler(func=lambda callback: callback.data == constants.menu_button_names[0])
    def return_call_back(callback):
        bot.send_message(callback.message.chat.id, "Давай начнем!")

    @bot.callback_query_handler(func=lambda callback: callback.data == "В меню")
    def callback_menu_handler(callback: CallbackQuery):
        print(callback.message.text)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=menu_markup)
        config.is_talking = False

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.TALK_WITH_BOT)
    def talk_call_back(callback):
        bot.send_message(callback.message.chat.id, "Write me something...")
        config.is_talking = True

    @bot.message_handler(content_types=['text'])
    def game_handler(message: Message):
        if game_manager.is_playing:
            tools.game_handler(bot, game_manager, message)
        elif config.is_talking:
            tools.talk_handler(bot, message)
        else:
            tools.translate_handler(bot, message)

    bot.polling()


if __name__ == "__main__":
    main()
