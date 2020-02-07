import telebot
import const
import weather
import logging
import bot_answers
import translator

bot = telebot.TeleBot(const.botAPI)

# start debug log
logging.basicConfig(filename='log_weather.log', level=logging.DEBUG)
logging.debug('current_weather')

##### KEYBOARDS #####
keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard1.row('Погода')
keyboard1.row('Переводчик')
ruen = 'С 🇷🇺 на 🇺🇸'
enru = 'С 🇺🇸 на 🇷🇺'
keyboard4 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard4.row(ruen, enru)


@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text.startswith('Погода'):
        get_weather(message)
    if message.text.startswith('Переводчик'):
        get_translation(message)

##### TRANSLATOR #####
@bot.message_handler(commands=['translator'])
def get_translation(message):
    msg = bot.send_message(message.chat.id, bot_answers.select_lang_message, reply_markup=keyboard4
                           )
    bot.register_next_step_handler(msg, choose_lang_trans)
    print(msg)

def choose_lang_trans(message):
    src = ''
    dst = ''
    if message.text == enru:
        src = 'en'
        dst = 'ru'
    elif message.text == ruen:
        src = 'ru'
        dst = 'en'

    bot.send_message(message.chat.id, bot_answers.input_text_to_translate)
    bot.register_next_step_handler(message, translate_text, src, dst)

def translate_text(message, src_lang, dest_lang):
    try:
        user_text = translator.get_translation(user_text=message.text, src_lang=src_lang, dest_lang=dest_lang
                                               )
    except Exception:
        user_text = bot_answers.translator_error_message
    bot.send_message(message.chat.id, user_text, reply_markup=keyboard1)

##### START MESSAGE #####
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, bot_answers.start_message)


##### HELP MESSAGE #####
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, bot_answers.help_message, reply_markup=keyboard1)


##### WEATHER #####
@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    bot_msg = bot.send_message(message.chat.id, bot_answers.select_city_message, reply_markup=gen_weather_markup())

    def call_custom_city(user_msg):
        weather_from_city(bot_msg.chat.id, user_msg.text, bot_msg.message_id, user_msg.message_id)

    bot.register_next_step_handler(bot_msg, call_custom_city)
    print(bot_msg)


@bot.callback_query_handler(lambda call: call.data.startswith('weather'))
def callback_query_weather(call):
    city = call.data.split('|')[1]
    weather_from_city(call.message.chat.id, city, call.message.message_id, 0)
    bot.clear_step_handler_by_chat_id(call.message.chat.id)


def weather_from_city(chat_id, city, message_id_bot, message_id_user):
    # This supports cities from inline buttons
    # and also a custom city from an user message.
    try:
        current_weather = weather.get_weather(city=city)
    except Exception:
        current_weather = bot_answers.select_city_error_message

    bot.edit_message_text(current_weather, chat_id, message_id_bot)
    if message_id_user != 0:
        bot.delete_message(chat_id, message_id_user)


def gen_weather_markup():
    markup = telebot.types.InlineKeyboardMarkup()

    def gen_button(city):
        return telebot.types.InlineKeyboardButton(city, callback_data='weather|' + city)

    markup.row(gen_button('Москва'))
    markup.row(gen_button('Санкт Петербург'))
    markup.row(gen_button('Екатеринбург'))
    markup.row(gen_button('Новосибирск'))
    return markup


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


bot.polling()
