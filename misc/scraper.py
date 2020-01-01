import requests
from bs4 import BeautifulSoup
import json
from myutil import Mail

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"}
text = ""

with open("scraper.json", "r") as f:
    products = json.load(f)

for product in products:
    URL = product
    buyprice = products[product]["buyprice"]
    try:
        pricewatch = products[product]["pricewatch"]
    except:
        pricewatch = False

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id="productTitle").get_text().strip()
    price = soup.find(id="priceblock_ourprice").get_text().strip()

    product_price = price.split(",")[0]
    product_price = float(product_price)

    # text = text + f"'{title}'\n\tConfigured buyprice: {buyprice} €\n\tCurrent price: {product_price} €"
    text = text + "'"+title+"'\n\tConfigured buyprice: "+str(buyprice)+" €\n\tCurrent price: "+str(product_price)+" €"

    if product_price <= buyprice:
        if pricewatch == False:
            print(text)
            products[product]["pricewatch"]=True
    elif product_price > buyprice:
        if pricewatch == True:
            print(text)
        products[product]["pricewatch"]=False


with open("scraper.json", "w") as f:
    json.dump(products, f)

email = Mail()
email.send("Price Monitoring", text, receipient)