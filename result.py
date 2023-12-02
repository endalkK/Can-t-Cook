import csv
import requests
from PIL import Image   

url = "http://127.0.0.1:5000/predict"
foodItems = list()

def convert(path):
    file = {'image': open(path,'rb')}
    response = requests.post(url, files=file)
    foodItems.append(response.json()['prediction'])
    #print(response.json())   

convert('48.jpg')
#convert('83.jpg')
#print(foodItems)

with open("archive/Food Ingredients and Recipe Dataset with Image Name Mapping.csv") as file:
    csvFile = csv.reader(file)
    next(csvFile)
    n=0
    for line in csvFile:
        #for item in foodItems:
        if foodItems[0] in line[2].split():
                print(line[3])         
                print("\n\n\n")                                                                   
                img = Image.open('archive/Food Images/Food Images/' + line[4] + '.jpg')
                img.show() 
                n+=1
                if n ==5:
                     break
    print(n)
            