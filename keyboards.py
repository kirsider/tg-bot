from telebot import types

import constants
import tools

menu_markup = tools.make_markup(constants.MENU_BUTTON_NAMES)

themes_markup = types.InlineKeyboardMarkup()
for i in constants.GAME_THEME_NAMES:
    themes_markup.row(types.InlineKeyboardButton(i, callback_data=i))
themes_markup.row(types.InlineKeyboardButton("В меню", callback_data="В меню"))

add_to_dict_markup = types.InlineKeyboardMarkup()
add_to_dict_markup.row(types.InlineKeyboardButton(constants.ADD_TO_DICT, callback_data=constants.ADD_TO_DICT))

play_markup = tools.make_markup(constants.PLAY_BUTTON_NAMES + ["В меню"])

nums_markup = types.InlineKeyboardMarkup()
num_buttons = []
for i in constants.POSSIBLE_NUMS:
    num_buttons.append(types.InlineKeyboardButton(str(i), callback_data=str(i)))
nums_markup.row(*num_buttons)

settings_markup = types.InlineKeyboardMarkup()
for i in constants.SETTINGS_OPTIONS:
    settings_markup.row(types.InlineKeyboardButton(i, callback_data=i))
settings_markup.row(types.InlineKeyboardButton("В меню", callback_data="В меню"))
