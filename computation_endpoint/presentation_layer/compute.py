from start_endpoint import app

@app.route('/ping', methods = ["GET"])
def ping():
    return "active"