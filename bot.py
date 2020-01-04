import telebot
import const
import weather
import logging
bot = telebot.TeleBot(const.botAPI)

# включить лог
# Где-то в начале.
#import logging
# Где-то один раз в файле.
#logging.basicConfig(filename='example.log',level=logging.DEBUG)
# Где-то где хочется что-то записать.
#logging.debug('Meh.')

logging.basicConfig(filename='log_weather.log',level=logging.DEBUG)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Меня зовут Мими, я очень полезная (нет)! Моя создательница '
                                      '@MiroslavaAutumn!'
                                      '\nЧтобы узнать, что я умею, введите /help!'
                     )

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Пока что я могу только узнавать погоду, но скоро научусь делать другие интересные вещи! '
                                      '\nНажмите на нужную кнопку!', reply_markup=keyboard1
                     )


keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard1.row('Погода', 'Пока')
keyboard2 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard2.row('Москва', 'Санкт-Петербург')
keyboard3 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard3.row('Да', 'Нет')

logging.debug('current_weather')
def sweather(message):
    try:
        current_weather = weather.get_weather(city=message.text)
    except Exception:
        current_weather = '\U000026D4 К сожалению, этот город не добавлен, или вы ввели неверное значение.' \
                          '\n\n\U0001F4A1 Попробуйте ввести город в английской раскладке!'
    bot.send_message(message.chat.id, current_weather, reply_markup=keyboard1)

@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    msg = bot.send_message(message.chat.id,
                           '\U0001F30D Выберите город из списка или введите вручную',reply_markup=keyboard2
                           )
    bot.register_next_step_handler(msg, sweather)
    print(msg)

@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'За пока бьют в бока \U0001f600')
    if message.text.lower() == 'привет':
        #bot.send_message(message.chat.id, 'Привет! Чем я могу тебе помочь?', reply_markup=keyboard1)
        bot.send_message(message.chat.id, 'Выбери ответ!', reply_markup=keyboard3)
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Пизда! \U0001f600', reply_markup=keyboard1)
    if message.text.lower() == 'нет':
        bot.send_message(message.chat.id, 'Пидора ответ! \U0001F468\U0000200D\U00002764\U0000FE0F\U0000200D\U0001F468', reply_markup=keyboard1)
    if message.text.startswith('Погода'):
        get_weather(message)

bot.polling()
