import pymongo
import telebot
from telebot.types import Message, CallbackQuery

import config
import constants
import db
import game
import keyboards
import model
import tools

TOKEN = '779969269:AAHV2ttOJ4bcYOfKDdcWty02cfzIh-0__W8'
bot = telebot.TeleBot(TOKEN)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['mydatabase']
words_dicts = mydb['words']


def choose_from_game_themes(point, game_manager: game.GameManager):
    @bot.callback_query_handler(func=lambda callback: callback.data == point)
    def callback_options_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Что делать?", reply_markup=keyboards.play_markup)
        d = words_dicts.find({'_id': point}).next()
        del (d['_id'])
        game_manager.set_pack(d, callback.message.chat.id)


def choose_game_nums(point):
    @bot.callback_query_handler(func=lambda callback: callback.data == point)
    def nums_call_back(callback: CallbackQuery):
        usr = db.find_record(callback.message.chat.id)
        c = usr['config']
        c['Количество вопросов в игре'] = int(point)
        db.delete_record(callback.message.chat.id)
        db.insert_record(callback.message.chat.id, usr['username'], c, usr['dictionary'],
                         usr['statistic'], usr['statlist'])

        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Данные изменены!\nВ меню: /menu")


def main():
    bot.delete_webhook()
    game_manager = game.GameManager()
    config.is_talking = False
    if 'users' not in mydb.list_collection_names():
        users = mydb['users']
        db.insert_record('0', 'none', {}, {}, {}, [])


    @bot.callback_query_handler(func=lambda callback: callback.data == "В меню")
    def callback_menu_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)

    @bot.callback_query_handler(func=lambda callback: callback.data == "Помощь")
    def callback_menu_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, constants.HELP_MESSAGE)

    @bot.message_handler(commands=['start'])
    def start_handler(message: Message):
        bot.send_message(message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)
        username = message.from_user.first_name + " " + message.from_user.last_name
        if 'users' in mydb.list_collection_names() and mydb['users'].find(
                {"user_id": message.from_user.id}).count() < 1:
            db.insert_record(message.from_user.id, username, constants.DEFAULT_CONFIG, {}, constants.DEFAULT_STATS, [])
            print("ok")

    @bot.message_handler(commands=['menu'])
    @bot.message_handler(func=lambda message: message.text == "В меню")
    def message_handler(message: Message):
        bot.send_message(message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)
        config.is_talking = False
        game_manager.is_playing = False

    @bot.message_handler(commands=['help'])
    @bot.message_handler(func=lambda message: message.text == "Помощь")
    def message_handler(message: Message):
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, constants.HELP_MESSAGE)

    @bot.callback_query_handler(func=lambda callback: callback.data == 'Играть')
    def game_theme_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Выберите тему:", reply_markup=keyboards.themes_markup)

    for item in constants.GAME_THEME_NAMES:
        choose_from_game_themes(item, game_manager)

    @bot.callback_query_handler(func=lambda callback: callback.data in constants.PLAY_BUTTON_NAMES)
    def play_handler(callback: CallbackQuery):
        if callback.data == constants.PLAY_BUTTON_NAMES[0]:
            game_manager.set_lang(constants.Languages.EN_RU, callback.message.chat.id)
        elif callback.data == constants.PLAY_BUTTON_NAMES[1]:
            game_manager.set_lang(constants.Languages.RU_EN, callback.message.chat.id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Поехали!")
        game_manager.users[callback.message.chat.id].is_playing = True
        usr = db.find_record(callback.message.chat.id)
        game_manager.get_guesses(usr['config']["Количество вопросов в игре"], callback.message.chat.id)
        game_manager.users[callback.message.chat.id].to_guess = next(
            game_manager.users[callback.message.chat.id].game_guesses)
        answers = game_manager.get_answers(game_manager.users[callback.message.chat.id].to_guess,
                                           callback.message.chat.id)
        game_manager.send_options(game_manager.users[callback.message.chat.id].to_guess, answers, bot,
                                  callback.message.chat.id)

    @bot.callback_query_handler(func=lambda callback: callback.data == "Играть")
    def callback_options_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Что делать?", reply_markup=keyboards.play_markup)

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.MENU_BUTTON_NAMES[0])
    def return_call_back(callback):
        bot.send_message(callback.message.chat.id, "Давай начнем!")

    @bot.callback_query_handler(func=lambda callback: callback.data == "В меню")
    def callback_menu_handler(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Меню:", reply_markup=keyboards.menu_markup)
        config.is_talking = False

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.TALK_WITH_BOT)
    def talk_call_back(callback):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id,
                         "Вы сейчас находитесь в диалоге с ботом. Чтобы выйти, отправте боту /menu.")
        bot.send_message(callback.message.chat.id, "Write me something...")
        config.is_talking = True

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.MY_DICT_BOT)
    def my_dict_call_back(callback):
        usr = db.find_record(callback.message.chat.id)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        d = usr['dictionary']
        m = "Мой словарь (" + usr['username'] + "):\n\n"
        for i in d.items():
            m += str(i[0]) + " -- " + str(i[1]) + '\n'
        m += '\nВернуться в меню: /menu'
        bot.send_message(callback.message.chat.id, m)

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.ADD_TO_DICT)
    def translate_call_back(callback: CallbackQuery):
        usr = db.find_record(callback.message.chat.id)
        wrds = callback.message.text.split('--')
        d = usr['dictionary']
        d[wrds[0][:-1]] = wrds[1][1:]
        db.delete_record(callback.message.chat.id)
        db.insert_record(callback.message.chat.id, usr['username'], usr['config'], d, usr['statistic'], usr['statlist'])
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Добавлено!")

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.SETTINGS_BOT)
    def settings_call_back(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Настройки:", reply_markup=keyboards.settings_markup)

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.DROP_ALL)
    def drop_call_back(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        usr = db.find_record(callback.message.chat.id)
        db.delete_record(callback.message.chat.id)
        db.insert_record(callback.message.chat.id, usr['username'], constants.DEFAULT_CONFIG, {},
                         constants.DEFAULT_STATS, [])
        bot.send_message(callback.message.chat.id, "Ваши данные были очищены!\nВ меню: /menu")

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.CHANGE_COUNT)
    def change_num_call_back(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, "Выберите новое количество вопросов:",
                         reply_markup=keyboards.nums_markup)

    for i in constants.POSSIBLE_NUMS:
        choose_game_nums(str(i))

    @bot.callback_query_handler(func=lambda callback: callback.data == constants.STATISTIC_BOT)
    def change_num_call_back(callback: CallbackQuery):
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        usr = db.find_record(callback.message.chat.id)
        stats = usr['statistic']
        verdict = model.verdict(callback.message.chat.id)
        if verdict != 'Позанимайтесь еще!':
            bot.send_photo(callback.message.chat.id, photo=open('plot.png', 'rb'))
        m = "Статистика (" + usr['username'] + "):\n\n"
        for i in stats.items():
            m += str(i[0]) + " : " + str(i[1]) + '\n'
        m += 'Вердикт : ' + verdict + '\n'
        m += '\nВернуться в меню: /menu'
        bot.send_message(callback.message.chat.id, m)


    @bot.message_handler(content_types=['text'])
    def game_handler(message: Message):
        if game_manager.users[message.chat.id].is_playing:
            tools.game_handler(bot, game_manager, message)
        elif config.is_talking:
            tools.talk_handler(bot, message)
        else:
            tools.translate_handler(bot, message)

    bot.polling()


if __name__ == "__main__":
    main()
