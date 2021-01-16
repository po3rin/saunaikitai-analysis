import requests
import math
import time
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://sauna-ikitai.com/search?"


def get_sauna_spec(soup):
    keys = [
        "loyly",
        "auto_loyly",
        "self_loyly",
        "out_air_bath",
        "break_space",
        "ion_water",
    ]
    spec_table = soup.find("table", class_="p-saunaSpecTable").find_all("tr")

    values = []
    for s in spec_table:
        v = s.find("img").get("alt")

        if v == "無し":
            v_hot = 0
        elif v == "有り":
            v_hot = 1

        values.append(v_hot)

    specs = {key: val for key, val in zip(keys, values)}
    return specs


def get_sauna_detail(soup):
    keys = [
        "open_24_hours",
        "capsule_hotel",
        "break_space_in",
        "restaurant",
        "wifi",
        "power_supply",
        "work_space",
        "comic",
        "body_care",
        "akasuri",
        "water_dispenser",
        "washlet",
        "credit_card_payment",
        "parking",
        "bedrock_bath",
        "tattoo",
        "shampoo",
        "conditioner",
        "body_soap",
        "face_soap",
        "razor",
        "toothbrush",
        "nylon_towel",
        "airdryer",
        "unlimited_use_face_towel",
        "unlimited_use_bath_towel",
        "unlimited_use_sauna_pants",
        "unlimited_use_sauna_mat",
        "unlimited_use_kickboard",
        "toner",
        "emulsion",
        "makeup_remover",
        "cotton_swab",
    ]

    spec_table = soup.find_all("li", class_="p-saunaSpecList_list")

    values = []
    for s in spec_table:
        v = s.find("span", class_="p-saunaSpecList_value").get_text()

        if v == "○":
            v_hot = 1
        elif v == "-":
            v_hot = 0

        values.append(v_hot)

    specs = {key: val for key, val in zip(keys, values)}
    return specs


def get_sauna_data():
    res = requests.get(BASE_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    total = soup.find("p", class_="p-result_number").find("span").get_text()
    pages = math.ceil(int(total) / 20)

    saunas = []

    # for debug
    pages = 0

    for p in range(pages + 1):
        res = requests.get(BASE_URL + f"?page={p}")
        soup = BeautifulSoup(res.text, "html.parser")
        contents = soup.find_all("div", class_="p-saunaItem p-saunaItem--list")

        for c in contents:
            name = c.find("h3").get_text().strip()
            url = c.find("a").get("href")
            res = requests.get(url)
            soup = BeautifulSoup(res.text, "html.parser")

            sauna_temp = (
                soup.find("div", class_="p-saunaSpecItem p-saunaSpecItem--sauna")
                .find("p", class_="p-saunaSpecItem_number")
                .find("strong")
                .get_text()
                .strip()
            )
            mizuburo_temp = (
                soup.find("div", class_="p-saunaSpecItem p-saunaSpecItem--mizuburo")
                .find("p", class_="p-saunaSpecItem_number")
                .find("strong")
                .get_text()
                .strip()
            )

            ikitai = (
                soup.find("div", class_="p-action_number js-ikitaiCounter")
                .get_text()
                .strip()
            )

            sauna = {
                "name": name,
                "sauna_temp": sauna_temp,
                "mizuburo_temp": mizuburo_temp,
                "ikitai": ikitai,
            }

            specs = get_sauna_spec(soup)
            sauna.update(specs)

            specs = get_sauna_detail(soup)
            sauna.update(specs)

            saunas.append(sauna)
            time.sleep(1)  # Avoid the load

        time.sleep(1)  # Avoid the load

    df = pd.DataFrame(saunas)
    print(df)


if __name__ == "__main__":
    get_sauna_data()
