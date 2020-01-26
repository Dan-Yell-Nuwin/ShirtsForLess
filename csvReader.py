import csv

class Product:
    def __init__(self, link, image, name, brand, gender, type_of, size, price):
        self.link = link
        self.image = image
        self.name = name
        self.brand = brand
        self.gender = gender
        self.type_of = type_of
        self.size = size
        self.price = price


with open('clothingProducts.csv', newline='') as csvfile:
    fileReader = csv.reader(csvfile, delimiter=',')
    reader = csv.reader(x.replace('\0', '') for x in csvfile)
    
    line = 0
    products = []
    
    for row in reader:
        if line == 0:
            line += 1
        else:
            if row is not None:
                link = row[0]
                image = row[1]
                name = row[2]
                brand = row[3]
                gender = row[4]
                type_of = row[5]
                size = row[6]
                price = row[7]
                
                products.append(Product(link, image, name, brand, gender, type_of, size, price))
        
keyword = "pants"
    
f = open('sustainablydressed.html', 'w')

header = """<html>
    <head>
        <link rel="stylesheet" type="text/css" href="wow.css">
    </head>
    <div class="header">
        <h3>Sustainably Dressed</h3>
    </div>
    """

f.write(header)

for product in products:
    if keyword in product.name:
        print("  found the word in " + product.name)
        
        wrapper = """<div>
            <img src='%s' width="300" height="300"</img>
            <a href=https://www.%s target="_blank"><h1>%s</h1></a>
            <h2>%s | $%s</h2>
            <h2>%s | %s</h2>
            </div>"""
            
        message = wrapper % (product.image, product.link, product.name, product.brand, product.price, product.gender, product.size)
            
        f.write(message)
f.close()