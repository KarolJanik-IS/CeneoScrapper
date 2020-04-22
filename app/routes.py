from app import app

@app.route("/")
@app.route("/index")
def index():
    return "Hello World"

@app.route("/scraper")
def scraper():
    return "Podaj kod produktu do pobrania opinii"

@app.route("/analyzer/<product_id>")
def analyzer():
    return "Podaj kod produktu do analizy"