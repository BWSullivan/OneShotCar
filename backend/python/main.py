# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
# -- ARGS --
API_KEY = 'ec8de34a-4d87-44c5-b569-3482f7a12858'
URL = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'
IMG_DIR = 'test-images/tesla-big.jpg'

# -- Query according to documentation --
query = {'accept': 'application/json',
         'api-key': API_KEY,
         'Content-Type': 'application/octet-stream'}

data = open(IMG_DIR, 'rb').read()
response = requests.post(URL, headers=query, data=data)

try:
    data = response.json() # parsing json answer
    detection_dict = data['detections']
    img_args = detection_dict[0]
    mmg = img_args['mmg']
    answer_dict = mmg[0]
    make_name = answer_dict['make_name']
    model_name = answer_dict['model_name']
    years = answer_dict['years']
    print(make_name, model_name, years)
except requests.exceptions.RequestException:
    print('error')
    print(response.text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
