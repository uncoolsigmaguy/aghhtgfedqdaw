from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

def scrape_site(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, headers=headers, timeout=5, verify=False)
        soup = BeautifulSoup(r.text, "html.parser")

        title = soup.title.text if soup.title else "No title"

        return {
            "url": url,
            "title": title
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

@app.route("/")
def home():
    return "Flask API running"

@app.route("/data")
def data():
    return jsonify({
        "site1": scrape_site("https://example.com"),
        "site2": scrape_site("https://example.org")
    })

if __name__ == "__main__":
    app.run()
