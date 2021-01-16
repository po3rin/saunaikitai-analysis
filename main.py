import requests
import math
import time
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = 'https://sauna-ikitai.com/search?'


def get_sauna_data():
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    total = soup.find('p', class_='p-result_number').find('span').get_text()
    pages = math.ceil(int(total) / 20)

    saunas = []

    # for debug
    pages = 0

    for p in range(pages+1):
        res = requests.get(BASE_URL+f'?page={p}')
        soup = BeautifulSoup(res.text, 'html.parser')
        contents = soup.find_all(
            'div', class_='p-saunaItem p-saunaItem--list')

        for c in contents:
            name = c.find('h3').get_text().strip()
            url = c.find('a').get('href')
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            sauna_temp = soup.find('div', class_='p-saunaSpecItem p-saunaSpecItem--sauna').find('p',
                                                                                                class_='p-saunaSpecItem_number').find('strong').get_text().strip()
            mizuburo_temp = soup.find('div', class_='p-saunaSpecItem p-saunaSpecItem--mizuburo').find('p',
                                                                                                      class_='p-saunaSpecItem_number').find('strong').get_text().strip()

            ikitai = soup.find(
                'div', class_='p-action_number js-ikitaiCounter').get_text().strip()

            sauna = {'name': name, 'sauna_temp': sauna_temp,
                     'mizuburo_temp': mizuburo_temp, 'ikitai': ikitai}
            saunas.append(sauna)
            time.sleep(1)  # Avoid the load

        time.sleep(1)  # Avoid the load

    df = pd.DataFrame(saunas)
    print(df)


if __name__ == '__main__':
    get_sauna_data()
