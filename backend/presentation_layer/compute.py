from start_endpoint import app

@app.route('/ping', methods = ["GET"])
def ping():
    """ chiamato per verificare che l'endpoint backand sia attivo e disponibile """
    return "active"