from telebot import types
import apiai, json
import translate
import game
import keyboards

AI_TOKEN = 'e8ad652f86584804a74a4fdf9c6804c8'


def translate_handler(bot, message: types.Message):
    ans = translate.translate(message.text)
    bot.send_message(message.chat.id, ans)


def game_handler(bot, game_manager: game.GameManager, message: types.Message):
    if message.text == game_manager.words[game_manager.to_guess]:
        bot.send_message(message.chat.id, "Правильно!")
        game_manager.counter += 1
    else:
        bot.send_message(message.chat.id, "Неправильно :(")
    game_manager.to_guess = next(game_manager.game_guesses, None)
    if game_manager.to_guess is None:
        game_manager.is_playing = False
        bot.send_message(message.chat.id, "Поздравляем! Вы набрали {0} из {1}!".format(
            game_manager.counter,
            game_manager.game_guesses_number), reply_markup=keyboards.menu_markup)

    else:
        answers = game_manager.get_answers(game_manager.to_guess)
        game_manager.send_options(game_manager.to_guess, answers, bot, message.chat.id)


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
