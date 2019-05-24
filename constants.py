from enum import Enum


class Languages(Enum):
    EN_RU = 0
    RU_EN = 1


NUM_OF_OPTIONS = 4

TALK_WITH_BOT = 'Поговорить с ботом'
PLAY_WITH_BOT = 'Играть'
LEARN_WITH_BOT = 'Начать изучение новых слов'
STATISTIC_BOT = "Статистика"
HELP_BOT = "Помощь"

menu_button_names = ['Начать изучение новых слов', 'Играть',
                     'Поговорить с ботом', 'Статистика',
                     'Помощь', 'Настройки']
