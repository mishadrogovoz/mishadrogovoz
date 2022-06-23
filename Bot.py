from email import message
import telebot
import requests
from bs4 import BeautifulSoup
import http.client


API_KEY = '5357462646:AAHzbZNIBl_Be9lSvDD8roWyVaBgG3eAVQY'

URL = "https://www.gismeteo.ua/weather-kyiv-4944/"

HEADERS = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "iframe",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "cross-site",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"}

temp = []
temp2 = []
temp3 = []

URL2 = "https://www.meteoprog.ua/ru/weather/Kyiv/"

URL3 = "https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2"

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_html2(url, params=None):
    r2 = requests.get(url, headers=HEADERS, params=params)
    return r2

def get_html3(url, params=None):
    r3 = requests.get(url, headers=HEADERS, params=params)
    return r3

def get_content(html):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="weathertabs")
    for item in items:
        temp.append({
            #"title": item.find("div", class_="tab-content").get_text(strip=True),
            'link': 'https://www.gismeteo.ua/weather-kyiv-4944/',
            "temperature": item.find("span", class_="unit_temperature_c").get_text(strip=True),
            "weather-feel": item.find("span", class_="measure").find("span", class_="unit_temperature_c").get_text(strip=True)
        })

def get_content2(html):
    soup2 = BeautifulSoup(html, "html.parser")
    items2 = soup2.find_all("section", class_="today-block")
    for item in items2:
        temp2.append({
            "link": "https://www.meteoprog.ua/ru/weather/Kyiv/",
            "temperature": item.find("div", class_="today-temperature").get_text(strip=True),
            "weather-feel": item.find("b").get_text(strip=True)
        })

def get_content3(html):
    soup3 = BeautifulSoup(html, "html.parser")
    items3 = soup3.find_all("div", class_="imgBlock")
    for item in items3:
        temp3.append({
            "link": "https://sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D0%B5%D0%B2",
            "temperature": item.find("p", class_="today-temp").get_text(strip=True),
            "weather-feel": item.find("p", class_="today-temp").get_text(strip=True)
        })

def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print("Error")

def parse2():
    html2 = get_html(URL2)
    if html2.status_code == 200:
        get_content2(html2.text)
    else:
        print("Error")

def parse3():
    html3 = get_html3(URL3)
    if html3.status_code == 200:
        get_content3(html3.text)
    else:
        print("Error")

parse()
parse2()
parse3()

bot = telebot.TeleBot(API_KEY)
@bot.message_handler(commands=['start'])

def hello(message):
    bot.send_message(message.chat.id, 'Привіт. Хочеш дізнатися погоду? Надрукуй Так')

@bot.message_handler(content_types=['text'])

def jokes(message):
    result = '; '.join([f'{key.capitalize()}: {value}' for key, value in temp[0].items()])
    bot.send_message(message.chat.id, result)
    result2 = '; '.join([f'{key.capitalize()}: {value}' for key, value in temp2[0].items()])
    bot.send_message(message.chat.id, result2)
    result3 = '; '.join([f'{key.capitalize()}: {value}' for key, value in temp3[0].items()])
    bot.send_message(message.chat.id, result3)

try:
    bot.polling(none_stop=True, interval=0)
except Exception:
    pass