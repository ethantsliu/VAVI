import requests

headers = {'Content-type': 'content_type_value'}

url = "https://eo33jqdqi6eyn70.m.pipedream.net/"

my_img = {'image': open('/Users/EthanLiu/Documents/Programming/Virtual Assistant/VAVI/TestData/smilingface.png', 'rb')}
r = requests.post(url, files=my_img, data={"question": "What species is this animal?"}, )

# convert server response into JSON format.

# url = "https://fe76-172-83-13-4.ngrok.io/vavi"
# r = requests.post(url) 

print(r)    
print(r.json())