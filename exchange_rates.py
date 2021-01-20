from pycoingecko import CoinGeckoAPI
from forex_python.converter import CurrencyRates

crypto = CoinGeckoAPI()
currency = CurrencyRates()


def get_exchange_rate():
    if what_coin.lower() == 'btc':
        btc = crypto.get_price(ids='bitcoin', vs_currencies='usd')
        current_rate = btc['bitcoin']['usd']
    elif what_coin.lower() == 'eth':
        eth = crypto.get_price(ids='ethereum', vs_currencies='usd')
        current_rate = eth['ethereum']['usd']
    elif what_coin.lower() == 'usd':
        usd = round(currency.get_rate('USD', 'RUB'), 2)
        current_rate = usd
    elif what_coin.lower() == 'eur':
        eur = round(currency.get_rate('EUR', 'RUB'), 2)
        current_rate = eur
    else:
        error = 'Введенные вами данные не поддерживаются'
        return error

    return current_rate


if __name__ == '__main__':
    what_coin = input('Какая монета?')
    result = get_exchange_rate()
    print(result)