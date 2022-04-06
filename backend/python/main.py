import requests

# -- KEYS and URLs --
API_KEY_carnet = 'ec8de34a-4d87-44c5-b569-3482f7a12858'
URL_carnet = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'

API_KEY_carinfo = 'haOKbNWT5dbmE1SAiFodnUbaMojtX75izMNdChLyulTuo3Ww1reCmA1CqEKR'

IMG_DIR = 'tesla-big.jpg'

# -- Query according to documentation --
query_carnet = {'accept': 'application/json',
         'api-key': API_KEY_carnet,
         'Content-Type': 'application/octet-stream'}

data = open(IMG_DIR, 'rb').read()
response = requests.post(URL_carnet, headers=query_carnet, data=data)

try:
    data = response.json()  # parsing json answer
    detection_dict = data['detections']
    img_args = detection_dict[0]
    probability = img_args['class']
    mmg = img_args['mmg']
    answer_dict = mmg[0]

    make_name = answer_dict['make_name']
    model_name = answer_dict['model_name']
    years = answer_dict['years']
    print(make_name, model_name, years)
    print(probability)

except requests.exceptions.RequestException:
    print('error')
    print(response.text)


response = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/models/2022/'+ make_name
                            + '?api_token=' + API_KEY_carinfo)

data = response.json()  # parsing json answer
print('Other models available today:')
for x in data:
    print(x['model'])

response = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/trims/2022/' + make_name + '/' + model_name + '/'
                            +'?api_token=' + API_KEY_carinfo)
data = response.json()  # parsing json answer
print('Trims available:')
for x in data:
    print(x['trim'])