import pyowm
import const
import statistics
import bot_answers
from weather_status import get_weather_status

owm = pyowm.OWM(const.owmAPI)

##### TEMPERATURE FORMAT #####
def format_temperature(w, t):
    temperature = w.get_temperature('celsius')[t]
    temperature = int(temperature)
    plus = '+' if temperature > 0 else ''
    return plus + str(temperature)


def get_weather(city):

    ##### LOCATION #####
    observation = owm.weather_at_place(city)
    w = observation.get_weather()

    ##### TEMPERATURE #####
    current_temperature = format_temperature(w, 'temp')
    max_temperature = format_temperature(w, 'temp_max')
    min_temperature = format_temperature(w, 'temp_min')

    ##### ADVICES #####
    advice = bot_answers.advice_message
    a = (statistics.mean([float(max_temperature), float(min_temperature)])
         )
    a = round(a)
    if a in range(-50, -30):
        advice = bot_answers.advice_message_1
    if a in range(-30, -20):
        advice = bot_answers.advice_message_2
    if a in range(-20, -10):
        advice = bot_answers.advice_message_3
    if a in range(-10, 0):
        advice = bot_answers.advice_message_4
    if a in range(0, 10):
        advice = bot_answers.advice_message_5
    if a in range(10, 18):
        advice = bot_answers.advice_message_6
    if a in range(18, 30):
        advice = bot_answers.advice_message_7
    if a in range(30, 40):
        advice = bot_answers.advice_message_8
    if a in range(40, 60):
        advice = bot_answers.advice_message_9
    else:
        bot_answers.advice_message

    ##### OTHER #####
    hum = w.get_humidity()
    wind = w.get_wind()['speed']

    ##### ANSWER #####
    answer = '\U0001F321 В городе {} сегодня ожидается{} до {}°C.{}'.format(
        city.title(),
        '' if min_temperature == max_temperature else ' от ' + min_temperature + '°C',
        max_temperature,
        '\nНа данный момент температура ' + current_temperature + '°C. '+ advice +
        '\n' + '\n🌀 Скорость ветра ' + str(wind) + 'м/с, относительная влажность воздуха ' + str(hum) + '%.'
        '\n' + '\n' + get_weather_status(str(w.get_detailed_status()))
    )

    return answer

if __name__ == '__main__':
    city = input('Какой город вас интересует?')
    result = get_weather(city)
    print(result)