from flask import render_template, request
from App.main import app
from App.scraper import scrape_url
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        result = scrape_url(url)
        return render_template("index.html", result=result)

    return render_template("index.html", result=None)
