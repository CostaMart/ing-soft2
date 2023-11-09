from flask import Flask

""" inizializza applicazione flask """
app = Flask(__name__)

""" importo il file in cui vengono definiti i metodi utilizzati dall'endpoint """
from presentation_layer.compute import *

if __name__ == '__main__':
    app.run(host='localhost', port=8080)