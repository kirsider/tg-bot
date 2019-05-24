import random
from telebot import types
import constants

family_dict = {
    "mother": "мама",
    "father": "папа",
    "son": "сын",
    "daughter": "дочь",
    "sister": "сестра",
    "brother": "брат",
    "grandfather": "дедушка",
    "grandmother": "бабушка",
}



class GameManager:
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

    def set_pack(self, words: dict, lang: constants.Languages):
        w = words
        if self.game_lang != lang:
            self.game_lang = lang
            v = list(words.values())
            k = list(words.keys())
            w = dict(zip(v, k))
        self.words = w
        self.all_answers = list(w.values())
        self.all_guesses = list(w.keys())
        self.counter = 0

    def get_answers(self, to_guess):
        answer = self.words[to_guess]
        options = [answer]
        possible_answers = self.all_answers

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

    def get_guesses(self, num_of_guesses):
        self.game_guesses_number = num_of_guesses
        self.game_guesses = iter(random.sample(self.all_guesses, num_of_guesses))






