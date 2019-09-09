from enum import Enum


class Languages(Enum):
    EN_RU = 0
    RU_EN = 1


NUM_OF_OPTIONS = 4

TALK_WITH_BOT = 'Поговорить с ботом'
PLAY_WITH_BOT = 'Играть'
MY_DICT_BOT = "Мой словарь"
STATISTIC_BOT = "Статистика"
HELP_BOT = "Помощь"
SETTINGS_BOT = "Настройки"

MENU_BUTTON_NAMES = [PLAY_WITH_BOT, TALK_WITH_BOT, MY_DICT_BOT,
                     STATISTIC_BOT, HELP_BOT, SETTINGS_BOT]

CHOOSE_EN_RU = 'Выбрать перевод с английского'
CHOOSE_RU_EN = 'Выбрать перевод с русского'

PLAY_BUTTON_NAMES = [CHOOSE_EN_RU, CHOOSE_RU_EN]

FAMILY_PACK = "Семья"
ANIMAL_PACK = "Животные"
HEALTH_PACK = "Человек и здоровье"
POPULAR_PACK = "Самые необходимые"
FOOD_PACK = "Еда"
NATURE_PACK = "Природа"
TRANSPORT_PACK = "Транспорт"
CLOTH_PACK = "Одежда"
TOWN_PACK = "Город"
PROFESSION_PACK = "Профессии"

GAME_THEME_NAMES = [FAMILY_PACK, ANIMAL_PACK, HEALTH_PACK,
                    POPULAR_PACK, FOOD_PACK, NATURE_PACK,
                    TRANSPORT_PACK, CLOTH_PACK, TOWN_PACK,
                    PROFESSION_PACK]

DEFAULT_STATS = {"Общий счет": 0,
                 "Всего": 0,
                 "Правильность": 0}

DEFAULT_CONFIG = {"Количество вопросов в игре": 5}

ADD_TO_DICT = "Добавить в словарь"

CHANGE_COUNT = "Количество вопросов в игре"
DROP_ALL = "Сбросить всё"
SETTINGS_OPTIONS = [CHANGE_COUNT, DROP_ALL]
POSSIBLE_NUMS = [5, 10, 15, 20, 25, 30]

HELP_MESSAGE = "Вас приветствует EnglishHelperBot!\n" \
               "Этот бот предназначен помочь в изучении английского языка." \
               "Чтобы начать играть, нажмите кнопку 'Играть'." \
               "Чтобы поговорить с ботом, нажмите кнопку 'Поговорить с ботом'." \
               "Чтобы перевести фразу с русского на английский или наоборот," \
               "просто отправте боту сообщение с текстом, который нужно перевести." \
               "Вы можете посмотреть свою Статистику и свой Словарь, а также изменить" \
               " поведение бота в Настройках.\n\n" \
               "Вернуться в меню: /menu"
