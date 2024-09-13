from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
def scrape_ebay(keyword):
    url = f"https://www.ebay.com/sch/i.html?_nkw={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    seen_products = set()

    for item in soup.select('.s-item'):
        title_element = item.select_one('.s-item__title')
        price_element = item.select_one('.s-item__price')
        link_element = item.select_one('.s-item__link')
        sponsor_element = item.select_one('.s-item__ad')

        if sponsor_element or title_element is None or price_element is None or link_element is None:
            continue

        title = title_element.get_text().strip()
        price = price_element.get_text().strip()
        link = link_element['href']
        if "Shop on eBay" in title and "$20.00" in price:
            continue

        if title not in seen_products:
            products.append({
                'title': title,
                'price': price,
                'link': link
            })
            seen_products.add(title)

    return products

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_products', methods=['POST'])
def get_products():
    keyword = request.form['keyword']
    
    products = scrape_ebay(keyword)
    
    return render_template('result.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
