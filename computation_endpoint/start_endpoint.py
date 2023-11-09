from flask import Flask



app = Flask(__name__)

@app.route('/ping', methods = ["GET"])
def ping():
    return "active"

if __name__ == '__main__':
    app.run(host='localhost', port=8080)