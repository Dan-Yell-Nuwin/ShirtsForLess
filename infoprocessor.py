import simplejson as json
import requests
import demoji
from bs4 import BeautifulSoup

filename = "clothingProducts.csv"
f = open(filename, "w", newline='', encoding="UTF-32BE")
headers = "link, image, name, brand, category, size, price\n"
f.write(headers)

# thredup
thred_up_sites = ['https://www.thredup.com/products/women?department_tags=women&sort=Newest%20First',
                  'https://www.thredup.com/products/girls?department_tags=girls&sort=Newest%20First',
                  'https://www.thredup.com/products/boys?department_tags=boys']

for site in thred_up_sites:
    thred_up_html = requests.get(site)
    soup = BeautifulSoup(thred_up_html.text, "html.parser")
    containers = soup.find_all("div", {"class": "results-grid-item"})
    if 'women' in site:
        category = 'Women'
    else:
        category = 'Kids'

    for container in containers:
        link = container.div.div.a["href"]
        data = json.loads(container.div.find('script', type='application/ld+json').text)
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
        f.write("thredup.com" + link + "," + img + "," + name + "," + brand + "," + category + "," + size + "\t," + str(price) + "\n")

# poshmark
poshmark_sites = ["https://poshmark.com/category/Men", "https://poshmark.com/category/Women", "https://poshmark.com/category/Kids"]
demoji.download_codes()

for sites in poshmark_sites:
    poshmark_html = requests.get(sites).text
    posh_soup = BeautifulSoup(poshmark_html, "html.parser")
    containers = posh_soup.findAll("div", {"class": "col-x12 col-l6 col-s8"})
    category = sites[sites.rindex('/') + 1:]

    for container in containers:
        link = "poshmark.com" + container.find("a")["href"]
        old_price = container.find("div", {"class": "price"}).text.strip()
        title = container.find("a", {"class": "title"}).text.strip()
        img = container.find("img")["src"]
        size = container.find("li", {"class": "size"}).text.strip()

        price = old_price[1:(old_price.rindex("$"))]
        title = title.replace(",", "，")
        title = demoji.replace(title)
        title = title.replace('’', '\'')

        if container.find("li", {"class": "size without-brand"}) is None:
            brand = container.find("li", {"class": "brand"}).text
        else:
            brand = "Assorted Brands"
        brand = brand.replace('’', '\'')

        # print(requests.get(sites).encoding)
        # if (requests.get(sites).encoding == "utf-8"):
        result = link + "," + img + "," + title + "," + brand + "," + category + "," + size[size.index('Size:') + 6:] + "\t," + price + "\n"
        # if (result.isprintable()):
        f.write(result)

    """
    print("\n")
    print("link: " + link)
    print("title: " + title)
    print("price: " + price)
    print("img: " + img)
    print("size: " + size)
    print("brand: " + brand)
    """
