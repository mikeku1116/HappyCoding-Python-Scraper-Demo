from bs4 import BeautifulSoup
import requests


response = requests.get("https://www.inside.com.tw/tag/AI")

soup = BeautifulSoup(response.content, "lxml")

cards = soup.find_all("div", {"class": "post_list_item"})

for card in cards:
    title = card.find("h3", {"class": "post_title"})
    published = card.find("li", {"class": "post_date"})

    print(f"標題：{title.getText().strip()}")
    print(f"日期：{published.getText().strip()}")
