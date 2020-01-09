import telebot
import const
import weather
import logging
import bot_answers

bot = telebot.TeleBot(const.botAPI)

# start debug log
logging.basicConfig(filename='log_weather.log', level=logging.DEBUG)
logging.debug('current_weather')

##### KEYBOARDS #####
keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard1.row('Погода', 'может ли робот написать симфонию, сделать шедевр?')
keyboard2 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard2.row('Москва', 'Санкт-Петербург')
keyboard3 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard3.row('Да', 'Нет')


##### START MESSAGE #####
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, bot_answers.start_message
                     )


##### HELP MESSAGE #####
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, bot_answers.help_message, reply_markup=keyboard1
                     )


##### WEATHER #####
def select_city(message):
    try:
        current_weather = weather.get_weather(city=message.text)
    except Exception:
        current_weather = bot_answers.select_city_error_message
    bot.send_message(message.chat.id, current_weather, reply_markup=keyboard1)


@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    msg = bot.send_message(message.chat.id, bot_answers.select_city_message, reply_markup=keyboard2
                           )
    bot.register_next_step_handler(msg, select_city)
    print(msg)


##### CHAT #####
@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'За пока бьют в бока \U0001f600')
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Выбери ответ!', reply_markup=keyboard3)
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Пизда! \U0001f600', reply_markup=keyboard1)
    if message.text.lower() == 'может ли робот написать симфонию, сделать шедевр?':
        bot.send_message(message.chat.id, 'Может! \U0001f600')
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Пидора ответ! '
                                          '\U0001F468\U0000200D\U00002764\U0000FE0F\U0000200D\U0001F468',
                         reply_markup=keyboard1)
    if message.text.startswith('Погода'):
        get_weather(message)


bot.polling()
