import requests

url = "http://127.0.0.1:5000/predict"
file = {'image': open('83.jpg', 'rb')}
response = requests.post(url, files=file)
print(response.json())  

url2 = "http://127.0.0.1:5000/recipe"
file2 = {
	"ingredients" : ["apple", "sugar"]
}
response2 = requests.post(url2, json=file2)
print(response2.json())   