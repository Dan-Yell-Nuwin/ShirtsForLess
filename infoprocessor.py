import simplejson as json
import requests
import demoji
from bs4 import BeautifulSoup

filename = "clothingProducts.csv"
f = open(filename, "w", newline='', encoding="UTF-32BE")
headers = "link, image, name, brand, gender, type, size, price\n"
f.write(headers)


def type_of_clothing(clothes):
    t_shirt_top = ['T-Shirt', 'Top', 'Bodysuit']
    pullover = ['Pullover', 'Sweater', 'Sweatshirt', 'Hoodie']
    shirt = ['Shirt', 'Blouse']
    dress = ['Dress', 'Romper', 'Jumpsuit', 'Skirt']
    coat = ['Coat', 'Cardigan', 'Jacket', 'Parka']
    trouser = ['Trousers', 'Pants', 'Jeans', 'Shorts']
    sandal = ['Sandals', 'Heels', 'Wedges', 'Pumps', 'Stilettos', 'Chacos', 'Flip Flop']
    ankle_boot = ['Boots']
    sneakers = ['Sneakers', 'Shoes']
    bag = ['Bag', 'Backpack', 'Purse']
    types = [t_shirt_top, pullover, shirt, dress, coat, trouser, sandal, ankle_boot, sneakers, bag]
    for arr in types:
        for entry in arr:
            if entry.lower() in clothes.lower():
                return arr[0]
    return 'None'


# thredup
thred_up_sites = ['https://www.thredup.com/products/women?department_tags=women&sort=Newest%20First',
                  'https://www.thredup.com/products/girls?department_tags=girls&sort=Newest%20First',
                  'https://www.thredup.com/products/boys?department_tags=boys']
thredup_count = 0;

for site in thred_up_sites:
    thred_up_html = requests.get(site)
    soup = BeautifulSoup(thred_up_html.text, "html.parser")
    containers = soup.find_all("div", {"class": "results-grid-item"})
    if 'women' in site:
        gender = 'Women'
    else:
        gender = 'Kids'

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
        type_of = type_of_clothing(name)
        price = data['offers']['price']
        
        print("   **searching through " + name + "...")
        print("      link: " + link)    
        print("      price: " + str(price))
        print("      gender: " + gender)
        print("      type: " + type_of)
        print("      brand: " + brand)
        print("      size: " + size)
        
        thredup_count += 1
        
        if type_of != 'None':
            f.write("thredup.com" + link + "," + img + "," + name + "," + brand + "," + gender + "," + type_of + "," + size + "\t," + str(price) + "\n")

print("scraped " + str(thredup_count) + "products from thredUp!")

# poshmark
poshmark_sites = ["https://poshmark.com/category/Men", "https://poshmark.com/category/Women",
                  "https://poshmark.com/category/Kids"]
demoji.download_codes()

posh_count = 0;

for sites in poshmark_sites:
    poshmark_html = requests.get(sites).text
    posh_soup = BeautifulSoup(poshmark_html, "html.parser")
    containers = posh_soup.findAll("div", {"class": "col-x12 col-l6 col-s8"})
    gender = sites[sites.rindex('/') + 1:]

    for container in containers:
        link = "poshmark.com" + container.find("a")["href"]
        old_price = container.find("div", {"class": "price"}).text.strip()
        title = container.find("a", {"class": "title"}).text.strip()
        type_of = type_of_clothing(title)
        img = container.find("img")["src"]
        size = container.find("li", {"class": "size"}).text.strip()

        price = old_price[1:(old_price.rindex("$"))]
        title = title.replace(",", "，")
        title = demoji.replace(title)
        title = title.replace('’', '\'')
        
        print("   **searching through " + title + "...")
        print("      link: " + link)    
        print("      price: " + price)
        print("      gender: " + gender)
        print("      type: " + type_of)

        if container.find("li", {"class": "size without-brand"}) is None:
            brand = container.find("li", {"class": "brand"}).text
        else:
            brand = "Assorted Brands"
        brand = brand.replace('’', '\'')
        
        print("      brand: " + brand)
        print("      size: " + size)
        
        posh_count += 1

        if type_of != 'None':
            f.write(link + "," + img + "," + title + "," + brand + "," + gender + "," + type_of + "," + size[size.index('Size:') + 6:] + "\t," + price + "\n")

print("scraped " + str(posh_count) + "products from poshmark!")

#ebay
ebay_sites = ["https://www.ebay.com/b/Mens-Clothing/1059/bn_696958", "https://www.ebay.com/b/Womens-Clothing/15724/bn_661783"]

for site in ebay_sites:
    my_html = requests.get(site)
    soup = BeautifulSoup(my_html.text, "html.parser")   
    items = soup.find("div",{"class":"dialog__cell"}).find("section",{"class":"b-module b-list b-categorynavigations b-display--landscape"}).find("ul").findAll("li") 
    
    ebay_count = 0


    categories = []
        
    items.pop(0)
    items.pop(0)

    for item in items:
        name = item.text
        if ((type_of_clothing(name) != "None") & (item.a["href"] is not None)):
            categories.append(item)
            print(name + " is valid!")
        
    for category in categories:
        category_title = category.text
        category_link = category.a["href"]
        print("  searching through " + category_title + "...")
        
        gender = category_title[0:category_title.find("'")]
        
        category_html = requests.get(category_link)
        category_soup = BeautifulSoup(category_html.text, "html.parser")
        
        #print(category_soup.find("ul",{"class":"b-list__items_nofooter"}).findAll("li"))
        
        products = category_soup.find("ul",{"class":"b-list__items_nofooter"}).findAll("li")
        
        for product in products:
            title = product.h3.text
            img = product.find("img")["src"]
            price = product.find("span",{"class":"s-item__price"}).text
            link = product.find("a")["href"]
            
            if (link[21:22] == 'i'):
            
                print("  **searching through " + title + "...")
                print("      link: " + link)
                print("      gender: " + gender)    
                print("      price: " + price)
                
                details_html = requests.get(link)
                details_soup = BeautifulSoup(details_html.text, "html.parser")
                
                #print("link broken down: " + link[21:22])
           
                details = details_soup.find("div",{"class":"section"}).find("table",{"role":"presentation"}).findAll("tr")

                for detail in details:
                    try:
                        brand = detail.find("h2").text
                        print("      brand: " + brand)
                        break
                    except:
                        pass
                
                try:
                    sizes = details_soup.find("select",{"name":"Size"}).findAll("option")
                except:
                    try:
                        gender_keyword = "Size (" + gender + "'s)"
                        sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                        break
                    except:
                        pass
                    try:
                        gender_keyword = "Size (" + gender + "s)"
                        sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                        break
                    except:
                        pass
                    try:
                        gender_keyword = "Size （" + gender + "'s）"
                        sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                        break
                    except:
                        pass
                    try:
                        gender_keyword = "Size （" + gender + "s）"
                        sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                        break
                    except:
                        pass
                
                try:
                    sizes.pop(0)
                except:
                    print("failed to pop")
                size = ""
                
                for choice in sizes:
                    if not choice.text.endswith(']'):
                        size += choice.text + " | "
                size = size[0:-2]        
                print("         size: " + size)
        ebay_count += 1
        
print("scraped " + ebay_count + " products from eBay!")

'''
                    try:
                        gender_keyword = "Size (" + gender + "'s)"
                        sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                    except:
                        try:
                            gender_keyword = "Size (" + gender + "s)"
                            sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                        except:
                            try:
                                gender_keyword = "Size （" + gender + "'s）"
                                sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                            except:
                                try:
                                    gender_keyword = "Size （" + gender + "s）"
                                    sizes = details_soup.find("select",{"name":gender_keyword}).findAll("option")
                                except:
                                    sizes = ["N/A"]
                                    '''

