from telebot import types
import constants
import tools

empty_markup = types.ReplyKeyboardMarkup()
empty_markup.row()

menu_markup = tools.make_markup(constants.menu_button_names)