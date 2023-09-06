import pyowm
import const
import statistics
import weather_status

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
    advice = weather_status.advice_messages[0]
    a = round(statistics.mean([float(max_temperature), float(min_temperature)]))
    temperatures = [-50, -30, -20, -10, 0, 10, 18, 30, 40, 60]
    for i, n in enumerate(temperatures):
        if a < n:
            advice = weather_status.advice_messages[i]
            break

    ##### OTHER #####
    hum = w.get_humidity()
    wind = w.get_wind()['speed']

    ##### ANSWER #####
    answer = '\U0001F321 В городе {} сегодня ожидается{} до {}°C.{}'.format(
        city.title(),
        '' if min_temperature == max_temperature else ' от ' + min_temperature + '°C',
        max_temperature,
        '\nНа данный момент температура ' + current_temperature + '°C. ' + advice +
        '\n' + '\n🌀 Скорость ветра ' + str(wind) + 'м/с, относительная влажность воздуха ' + str(hum) + '%.'
                                                                                                         '\n' + '\n' + weather_status.get_weather_status(
            str(w.get_detailed_status())))

    return answer


if __name__ == '__main__':
    city = input('Какой город вас интересует?')
    result = get_weather(city)
    print(result)
