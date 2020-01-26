import csv
import codecs

class Product:
    def __init__(link, image, name, brand, gender, type_of, size, price):
        self.link = link
        self.image = image
        self.name = name
        self.brand = brand
        self.gender = gender
        self.type_of = type_of
        self.size = size
        self.price = price



with open('clothingProducts.csv', newline='') as csvfile:
    fileReader = csv.reader(csvfile, delimiter=',', quotechar='|')
    reader = csv.reader(x.replace('\0', '') for x in csvfile)
    
    line = 0
    products = []
    
    for row in reader:
        if row is not None:
            data = row
            #data[0] = link
            #data[1] = image
            #data[2] = name
            #data[3] = brand
            #data[4] = gender
            #data[5] = type
            #data[6] = size
            #data[7] = price
            products.append(Product(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        
    #keyword = "shirt"
    
f = open('sustainablydressed.html', 'wb')

for product in products:
    print(product)
    if product.name.find("shirt") is not None:
        print("  found the word!")
         
        message = "<div><img="
        message += product.img + "width='300' height='300'</img><a href="
        message += product.link + "><h1>"
        message += product.name + "</h1></a><h2>"
        message += product.brand + " | " + product.type_of + "</h2><h2>"
        message += product.gender + " | " + product.size + "</h2><h3>"
        message += product.price + "</h3></div>"
            
f.write(message)
f.close()