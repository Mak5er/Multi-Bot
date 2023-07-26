from flask import Flask
from threading import Thread
import requests
import time

app = Flask('')

import flask.cli
flask.cli.show_server_banner = lambda *args: None


@app.route('/')
def main():
    return '>>>print("Hello, world!")'


def run():
    app.run(host="0.0.0.0", port=8080)  # don't touch this


def keep_alive():
    server = Thread(target=run)
    server.start()

def crawl_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            pass
        else:
            print(f"Помилка: не вдалося отримати сторінку. Код статусу: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Помилка: {e}")

def run_crawler(url, interval):
    while True:
        crawl_page(url)
        time.sleep(interval)

def start_crawling():
    urls = ["https://joke-bot.mak5er.repl.co/", "https://multi-bot.mak5er.repl.co/"]
    for url_to_crawl in urls:
        print(url_to_crawl)
        crawl_thread = Thread(target=run_crawler, args=(url_to_crawl, 30))
        crawl_thread.daemon = True
        crawl_thread.start()
