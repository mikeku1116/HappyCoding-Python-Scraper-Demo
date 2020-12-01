from bs4 import BeautifulSoup
import grequests
import pymysql

stocks = ["2330", "2454", "2451"]

links = []
for stock in stocks:
    links.append(f"https://tw.stock.yahoo.com/q/q?s={stock}")

reqs = (grequests.get(link) for link in links)
resps = grequests.imap(reqs, grequests.Pool(3))

results = []
for r in resps:

    soup = BeautifulSoup(r.text.replace("加到投資組合", ""), "lxml")
    stock_date = soup.find("font", {"class": "tt"}).getText()[-9:]

    tables = soup.find_all("table")[2]
    tds = tables.find_all("td")[0:11]

    stock_data = tuple(td.getText().strip() for td in tds)
    results.append((stock_date,) + stock_data)

print(results)

# 資料庫連線設定(替換成自己的)
db_settings = {
    "host": "us-cdbr-east-02.cleardb.com",
    "port": 3306,
    "user": "b3bff0a42ec79b",
    "password": "255f3ebb",
    "db": "heroku_035b57eec5a3f5a",
    "charset": "utf8"
}

conn = pymysql.connect(**db_settings)
with conn.cursor() as cursor:
    sql = """INSERT INTO market(
                market_date,
                stock_name,
                market_time,
                final_price,
                buy_price,
                sell_price,
                ups_and_downs,
                lot,
                yesterday_price,
                opening_price,
                highest_price,
                lowest_price)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    for result in results:
        cursor.execute(sql, result)
    conn.commit()
