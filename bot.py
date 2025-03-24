import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "7963160473:AAH49fQqUZIQS_5fcFhmqJeLQ-a8tb2qi6M"  # <<<<< BU YERGA BOT TOKENINGIZNI KIRITING
YANDEX_SEARCH_URL = "https://yandex.com/search/?text={query}"

bot = telebot.TeleBot(TOKEN)

def search_yandex(query):
    """ Yandex orqali qidiruv natijalarini olish """
    url = YANDEX_SEARCH_URL.format(query=query)
    headers = {"User-Agent": "Mozilla/5.0"}  # Brauzer emulyatsiyasi

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        return ["Xatolik yuz berdi!"]

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.startswith("http") and "yabs.yandex" not in href:
            results.append(href)
        if len(results) >= 5:  # Maksimal 5 ta natija olish
            break

    return results if results else ["Hech narsa topilmadi!"]

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "👋 Salom! Menga so‘rov yuboring va men uni Yandex'da qidirib beraman!")

@bot.message_handler(func=lambda message: True)
def handle_query(message):
    bot.send_message(message.chat.id, f"🔎 '{message.text}' bo‘yicha qidirmoqdamiz...")
    
    results = search_yandex(message.text)
    
    reply = "\n".join(results)
    bot.send_message(message.chat.id, reply)

if __name__ == "__main__":
    bot.polling(none_stop=True)
