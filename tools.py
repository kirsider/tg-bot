import apiai
import json
from telebot import types

import db
import game
import keyboards
import translate

AI_TOKEN = 'e8ad652f86584804a74a4fdf9c6804c8'


def translate_handler(bot, message: types.Message):
    ans = message.text + " -- " + translate.translate(message.text)
    bot.send_message(message.chat.id, ans, reply_markup=keyboards.add_to_dict_markup)


def game_handler(bot, game_manager: game.GameManager, message: types.Message):
    if message.text == game_manager.users[message.chat.id].words[game_manager.users[message.chat.id].to_guess]:
        bot.send_message(message.chat.id, "Правильно!")
        game_manager.users[message.chat.id].counter += 1
    else:
        bot.send_message(message.chat.id, "Неправильно :(")
    game_manager.users[message.chat.id].to_guess = next(game_manager.users[message.chat.id].game_guesses, None)
    if game_manager.users[message.chat.id].to_guess is None:
        game_manager.users[message.chat.id].is_playing = False
        bot.send_message(message.chat.id, "Поздравляем! Вы набрали {0} из {1}!\nВернутся в меню: /menu".format(
            game_manager.users[message.chat.id].counter,
            game_manager.users[message.chat.id].game_guesses_number), reply_markup=types.ReplyKeyboardRemove())
        usr = db.find_record(message.chat.id)

        stats = usr['statistic']
        slist = usr['statlist']
        slist.append(
            game_manager.users[message.chat.id].counter / game_manager.users[message.chat.id].game_guesses_number)
        stats['Общий счет'] += game_manager.users[message.chat.id].counter
        stats['Всего'] += game_manager.users[message.chat.id].game_guesses_number
        stats['Правильность'] = str(int(round(stats['Общий счет'] / stats['Всего'], 2) * 100)) + "%"

        db.delete_record(message.chat.id)
        db.insert_record(message.chat.id, usr['username'], usr['config'], usr['dictionary'], stats, slist)
    else:
        answers = game_manager.get_answers(game_manager.users[message.chat.id].to_guess, message.chat.id)
        game_manager.send_options(game_manager.users[message.chat.id].to_guess, answers, bot, message.chat.id)


def make_markup(button_names):
    markup = types.InlineKeyboardMarkup()
    for it in button_names:
        markup.row(types.InlineKeyboardButton(text=it, callback_data=it))
    return markup


def talk_handler(bot, message: types.Message):
    request = apiai.ApiAI(AI_TOKEN).text_request()
    request.lang = 'en'
    request.session_id = 'EnglishHelperBot'
    request.query = message.text
    response_json = json.loads(request.getresponse().read().decode('utf-8'))
    response = response_json['result']['fulfillment']['speech']
    if response:
        bot.send_message(chat_id=message.chat.id, text=response)
    else:
        bot.send_message(chat_id=message.chat.id, text="I don't understand :(")
