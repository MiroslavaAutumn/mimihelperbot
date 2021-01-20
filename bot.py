import telebot
import const
import weather
import exchange_rates

bot = telebot.TeleBot(const.botAPI)

##### START MESSAGE ####################################################################################################
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет! Меня зовут Мими, я очень полезная! Моя создательница @MiroslavaAutumn! '
        '\nЧтобы узнать, что я умею, введите /help! \n')


##### HELP MESSAGE #####################################################################################################
@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Пока что я могу только узнавать погоду, но скоро научусь делать другие '
                                      'интересные вещи!\nНажмите на нужную кнопку!', reply_markup=keyboard1)


##### KEYBOARDS ########################################################################################################
keyboard1 = telebot.types.ReplyKeyboardMarkup(False, True)
keyboard1.row('🌦 Погода 🌦')
keyboard1.row('💰 Курсы валют 💰')
keyboard1.row('🇷🇺 Переводчик 🇺🇸')
keyboard1.row('😁 Мими, пошути! 😁')

########################################################################################################################
@bot.message_handler(content_types=['text'])
def send_text(message):
    print(message.text)
    if message.text.startswith('🌦 Погода 🌦'):
        get_weather(message)
    if message.text.startswith('🇷🇺 Переводчик 🇺🇸'):
        get_translation(message)
    if message.text.startswith('💰 Курсы валют 💰'):
        get_exchange_rate(message)
    if message.text.startswith('😁 Мими, пошути! 😁'):
        get_joke(message)


##### WEATHER ##########################################################################################################
@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    bot_msg = bot.send_message(message.chat.id,
                               '\U0001F30D Выберите город из списка или введите вручную',
                               reply_markup=gen_weather_markup())

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
        current_weather = '\U000026D4 К сожалению, этот город не добавлен, или вы ввели неверное значение.' \
                          '\n\n\U0001F4A1 Попробуйте ввести город в английской раскладке!'

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


##### EXCHANGE RATE ####################################################################################################
@bot.message_handler(commands=['er'])
def get_exchange_rate(message):
    bot_msg = bot.send_message(message.chat.id,
                               'Выберите валюту.\n Для USD и EUR будет показан курс к рублю, для крипты - к доллару.',
                               reply_markup=gen_er_markup())

    def call_currency(user_msg):
        select_currency(bot_msg.chat.id, user_msg.text, bot_msg.message_id, user_msg.message_id)

    bot.register_next_step_handler(bot_msg, call_currency)
    print(bot_msg)


@bot.callback_query_handler(lambda call: call.data.startswith('er'))
def callback_query_currency(call):
    coin = call.data.split('|')[1]
    select_currency(call.message.chat.id, coin, call.message.message_id, 0)
    bot.clear_step_handler_by_chat_id(call.message.chat.id)


def select_currency(chat_id, coin, message_id_bot, message_id_user):
    try:
        current_er = exchange_rates.get_exchange_rate(coin=coin)
    except Exception:
        current_er = '\U000026D4 Ошибка! Выберите вариант из предложенных!'

    bot.edit_message_text(current_er, chat_id, message_id_bot)
    if message_id_user != 0:
        bot.delete_message(chat_id, message_id_user)


def gen_er_markup():
    markup = telebot.types.InlineKeyboardMarkup()

    def gen_button(cur_board):
        return telebot.types.InlineKeyboardButton(cur_board, callback_data='er|' + cur_board)

    markup.row(gen_button('USD'))
    markup.row(gen_button('EUR'))
    markup.row(gen_button('BTC'))
    markup.row(gen_button('ETH'))
    return markup


#### TRANSLATOR ########################################################################################################
@bot.message_handler(commands=['translator'])
def get_translation(message):
    bot.send_message(
        message.chat.id,
        'Функционал переводчика будет добавлен позднее.')


##### JOKE #############################################################################################################
@bot.message_handler(commands=['joke'])
def get_joke(message):
    bot.send_message(
        message.chat.id,
        'Купил мужик шляпу, а она ему как раз! \n\n Скоро я научусть шутить смешнее!')


########################################################################################################################


if __name__ == '__main__':
    bot.polling(none_stop=True)
