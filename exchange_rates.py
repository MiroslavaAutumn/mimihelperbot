from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_exchange_rate():
    if what_coin.lower() == 'btc':
        btc = cg.get_price(ids='bitcoin', vs_currencies='usd')
        current_rate = btc['bitcoin']['usd']
    elif what_coin.lower() == 'eth':
        eth = cg.get_price(ids='ethereum', vs_currencies='usd')
        current_rate = eth['ethereum']['usd']
    else:
        error = 'Введенные вами данные не поддерживаются'
        return error

    return current_rate


if __name__ == '__main__':
    what_coin = input('Какая монета?')
    result = get_exchange_rate()
    print(result)