import requests
from bs4 import BeautifulSoup

#product_code = input("Podaj kod produtu")
product_code = "96685108"
url =f'https://www.ceneo.pl/{product_code}#tab=reviews'
response = requests.get(url)
page = BeautifulSoup(response.text, 'html.parser')
opinions = page.select('div.js_product-review')

for opinion in opinions:
    print(opinion['data-entry-id'])