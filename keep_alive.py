from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return '>>>print("Hello, world!")'


def run():
    app.run(host="0.0.0.0", port=0000)  # don't touch this


def keep_alive():
    server = Thread(target=run)
    server.start()
