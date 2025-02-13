from flask import Flask, render_template, request, jsonify
from scraping.scraper import scrape_website

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scrape', methods=['GET'])
def scrape():
    result = scrape_website()  # Ahora extrae directamente de Investing.com
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)