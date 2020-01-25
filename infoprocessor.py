import simplejson as json
import requests
from bs4 import BeautifulSoup

#thredup
thred_up_html = requests.get('https://www.thredup.com/products/women?department_tags=women&sort=Newest%20First')
soup = BeautifulSoup(thred_up_html.text, "html.parser")
containers = soup.find_all("div", {"class": "results-grid-item"})

filename = "clothingProducts.csv"
f = open(filename, "w", newline='', encoding="utf-32be")
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

#poshmark
poshmark_sites = ["https://poshmark.com/category/Men","https://poshmark.com/category/Women"]

for sites in poshmark_sites:
    poshmark_html = requests.get(sites).text
    posh_soup = BeautifulSoup(poshmark_html, "html.parser")
    containers = posh_soup.findAll("div",{"class":"col-x12 col-l6 col-s8"})

    for container in containers:
        link = "poshmark.com" + container.find("a")["href"]
        old_price = container.find("div",{"class":"price"}).text.strip()
        title = container.find("a",{"class":"title"}).text.strip()
        img = container.find("img")["src"]
        size = container.find("li",{"class":"size"}).text.strip()
        
        price = old_price[1:(old_price.rindex("$"))].strip()
        title = title.replace("," ,"，")
        
        if(container.find("li",{"class":"size without-brand"}) is None):
            brand = container.find("li",{"class":"brand"}).text
        else:
            brand = "Assorted Brands"
            
        #print(requests.get(sites).encoding)
        
        #if (requests.get(sites).encoding == "utf-8"):
        result = link + "," + img + "," + title + "," + brand + "," + size + "," + price + "\n"
        #if (result.isprintable()):
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