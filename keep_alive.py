import os

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return '>>>print("Hello, world!")'


def run():
    app.run(debug=True, port=os.getenv("PORT", default=5000))  # don't touch this


def keep_alive():
    server = Thread(target=run)
    server.start()
