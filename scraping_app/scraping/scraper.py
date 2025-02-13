import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.find("title").text
        return {"title": title, "status": "Success"}
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

