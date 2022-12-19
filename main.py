import schedule
import time

import urllib.request
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os

try:
    load_dotenv()
except:
    pass

with open('log.txt', 'w') as fp:
    pass

log = ""

def check_availability(url, phrase):
    global log
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features="html.parser")

        if phrase in soup.text:
            return False
        return True
    except Exception as e:
        log += str(e)
        print(e)


def main():
    global log
    url = os.environ.get("URL")
    phrase = "Stock Awaited"
    available = check_availability(url, phrase)

    success = "Watch seems to be available"
    logfile = open('log.txt', "r+")

    if success in logfile.read():
        print("Watch already found in  stock")
        return
    
    if available:
        log += success
        try:
            bot_token = os.environ.get("BOT_TOKEN")
            chat_id = os.environ.get("CHAT_ID")
            send_text = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=MarkdownV2&text=In Stock"
            response = requests.get(send_text)
        except Exception as e:
            log += str(e)
            print(e)
    else:
        log += "No watch seems to be available"
    logfile.write(str(datetime.now()) + " " + log + "\n")
    log = " "
    logfile.close()


if __name__ == "__main__":
    schedule.every(600).seconds.do(main)

    while 1:
        schedule.run_pending()
        time.sleep(1)