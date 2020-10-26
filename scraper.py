from bs4 import BeautifulSoup
import requests


response = requests.get("https://www.inside.com.tw/tag/AI")

soup = BeautifulSoup(response.content, "lxml")

# 爬取文章標題
titles = soup.find_all("h3", {"class": "post_title"})

for title in titles:
    print(title.getText().strip())
