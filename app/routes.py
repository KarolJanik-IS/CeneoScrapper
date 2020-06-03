from app import app
from flask import render_template,request,redirect,url_for
from flaskext.markdown import Markdown
from app.forms import ProductForm
from app.models import Product,Opinion
import pandas as pd
import requests
app.config['SECRET_KEY'] = "Tajemniczy_mysi_sprzęt"

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    content = ""
    with open("README.md", "r" ,encoding="utf-8") as f:
        content = f.read()
    return render_template("about.html", text = content)

@app.route("/extract", methods = ["POST", "GET"])
def extract():
    form = ProductForm()
    if form.validate_on_submit():
        page_response = requests.get("https://www.ceneo.pl/"+request.form["product_code"])
        print("problem " + str(page_response.status_code))
        print(str(form.product_code))
        if  page_response.status_code == 200:
            product = Product(request.form['product_code'])
            product.extract_product()
            product.save_product()
            return redirect(url_for("product", product_id=product.product_id))
        else: 
            form.product_code.errors.append("Dla podanego kodu nie ma produktu")
            return render_template("extract.html",form = form)
        # return "Przesłano formularz"
    return render_template("extract.html", form=form)
    # if request.method == "POST":
    #     return "Przesłano formularz"
    # form = ProductForm()
    # return render_template("extract.html", form = form)

@app.route("/products")
def products():
    return "Podaj kod produktu do pobrania opinii"

@app.route('/product/<product_id>')
def product(product_id):
    product = Product(product_id)
    product.read_product()
    opinions = pd.DataFrame.from_records([opinion.__dict__() for opinion in product.opinions])
    # opinions = opinions.set_index("opinion_id")
    opinions["stars"] = opinions["stars"].map(lambda x: float(x.split("/")[0].replace(",", ".")))
    return render_template("product.html", tables=[
        opinions.to_html(
            classes='table table-bordered table-sm table-responsive',
            table_id="opinions"
        )
    ])
    # return str(product)

@app.route("/analyzer/<product_id>")
def analyzer():
    return "Podaj kod produktu do analizy"