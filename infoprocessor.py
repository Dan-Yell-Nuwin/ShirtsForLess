import simplejson as json
import requests
from bs4 import BeautifulSoup

page_html = requests.get('https://www.thredup.com/products/women?department_tags=women&sort=Newest%20First')
soup = BeautifulSoup(page_html.text, "html.parser")
containers = soup.find_all("div", {"class": "results-grid-item"})

filename = "thredup.csv"
f = open(filename, "w")
headers = "link, image, name, brand, size, price\n"
f.write(headers)

for container in containers:
    link = container.div.div.a["href"]
    data = json.loads(container.find('script', type='application/ld+json').text)
    img = data['image'][0]
    brand = data['brand']['name']
    if "Size" in data['description']:
        size = data['description'][data['description'].index('Size') + 5:]
    elif "Waist" in data['description']:
        size = data['description'][data['description'].index('Waist') - 3:data['description'].index('Waist') - 1]
    else:
        size = 'One size/No size'
    name = data['name']
    price = data['offers']['price']
    f.write("thredup.com" + link + "," + img + "," + name + "," + brand + "," + size + "," + str(price) + "\n")
