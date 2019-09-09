import random

from telebot import types

import constants


class User:
    def __init__(self):
        self.words = None
        self.all_guesses = None
        self.all_answers = None
        self.game_guesses = None
        self.game_answers = None
        self.is_playing = False
        self.to_guess = None
        self.game_guesses_number = None
        self.game_lang = constants.Languages.EN_RU
        self.counter = 0


class GameManager:
    def __init__(self):
        self.users = {}

    def set_pack(self, words: dict, user_id):
        usr = User()
        usr.words = words
        usr.all_answers = list(words.values())
        usr.all_guesses = list(words.keys())
        usr.counter = 0
        self.users[user_id] = usr

    def set_lang(self, lang: constants.Languages, user_id):
        usr = self.users[user_id]
        if usr.game_lang != lang:
            usr.game_lang = lang
            v = list(usr.words.values())
            k = list(usr.words.keys())
            w = dict(zip(v, k))
            usr.words = w
            usr.all_answers = list(w.values())
            usr.all_guesses = list(w.keys())

    def get_answers(self, to_guess, user_id):
        usr = self.users[user_id]
        answer = usr.words[to_guess]
        options = [answer]
        possible_answers = usr.all_answers

        for i in range(constants.NUM_OF_OPTIONS - 1):
            opt = answer

            while opt == answer:
                opt = random.choice(possible_answers)

            options.append(opt)

        random.shuffle(options)
        return options

    def send_options(self, correct, answers, bot, user_id):
        markup = types.ReplyKeyboardMarkup()
        markup.row(types.KeyboardButton(answers[0]), types.KeyboardButton(answers[1]))
        markup.row(types.KeyboardButton(answers[2]), types.KeyboardButton(answers[3]))
        bot.send_message(user_id, correct, reply_markup=markup)

    def get_guesses(self, num_of_guesses, user_id):
        usr = self.users[user_id]
        usr.game_guesses_number = num_of_guesses
        usr.game_guesses = iter(random.sample(usr.all_guesses, num_of_guesses))
