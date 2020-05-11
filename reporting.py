import webbrowser
from threading import Timer

from flask import Flask, render_template
from helper import read_json_keys
import constants

app = Flask(__name__)


@app.route("/")
def broken_links_page():
    dictionary = read_json_keys()
    if len(dictionary) == 0:
        return render_template('no_broken_links.html')
    else:
        return render_template('broken_links.html', dict=dictionary)


def open_browser():
    webbrowser.open_new(constants.HOST_URL)


def create_reporting():
    Timer(1, open_browser).start()
    app.run(port=5000)
