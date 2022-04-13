import requests


def get_other_models():  # done
    response_model = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/models/2022/' + make_name
                                      + '?api_token=' + API_KEY_carinfo)

    other_models = response_model.json()  # parsing json answer
    model_list = []
    for model in other_models:
        model_list.append(model['model'])
    return model_list


def get_trims():
    response_trim = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/trims/' + years_first + '/'
                                     + make_name + '/' + model_name + '/' + '?api_token=' + API_KEY_carinfo)

    trims_ = response_trim.json()  # parsing json answer
    trim_list = []
    for trim in trims_:
        trim_list.append(trim['trim'])
    return trim_list


def get_transmissions(list_trims):  # O(n^2) avg case, this takes forever. Not sure if there is another way
    # might switch data structures to get O(lg n)
    list_of_trans = []
    for selected_trim in list_trims:
        response_trans = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/car/transmissions/'
                                          + years_first + '/' + make_name + '/' + model_name + '/' + selected_trim +
                                          '?api_token=' + API_KEY_carinfo)
        transmissions = response_trans.json()

        for trans in transmissions:
            try:
                if trans['transmission'] not in list_of_trans:
                    list_of_trans.append(trans['transmission'])
            except TypeError:
                print("None found!")
    return list_of_trans


# -- KEYS and URLs --
API_KEY_carnet = 'ec8de34a-4d87-44c5-b569-3482f7a12858'
URL_carnet = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'

API_KEY_carinfo = 'haOKbNWT5dbmE1SAiFodnUbaMojtX75izMNdChLyulTuo3Ww1reCmA1CqEKR'
IMG_DIR = 'sedna.jpg'

# -- VALUES AFTER RUN --
# main():
#   probability: Double, contains probability in percentage of carnetAPI
#   make_name: String, contains make name
#   model_name: String, contains model name
#   years_first: String, contains first model year
#   year_last: String, contains last model year (might be empty if car generation is still in production)

# get_other_models():
#   other_models_today: String list, contains other models from selected make in 2022

# get_trims():
#   trims: String list, contains other trims from selected model

# get_power_train():
#   power_train: String list, contains different power-trains from selected model

# get_transmission():


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
    amg = img_args['class']
    probability = amg['probability'] * 100

    mmg = img_args['mmg']
    answer_dict = mmg[0]

    make_name = answer_dict['make_name']

    # Some answers come in from API like this: Accord (North America)
    # so to get rid of '(<location>)' we split as shown below.
    # This works even if answer doesn't have location.

    model_name_location = answer_dict['model_name']
    model_name_list = model_name_location.split('(')
    model_name = model_name_list[0]  # throw away location

    # years comes in from API like this: 1997 - 2018

    years = answer_dict['years']
    years_list = years.split('-')
    years_first = years_list[0]
    years_last = years_list[1]
    for x in years_list:
        print(x)

    print(make_name, model_name, years)
    print(probability)

except requests.exceptions.RequestException:
    print('error')
    print(response.text)

# -- TEST AREA --
print("")
print('Testing other models')
other_models_today = get_other_models()
for x in other_models_today:
    print(x)

print("")
print('Testing trims')
trims = get_trims()
for x in trims:
    print(x)

print("")
print('Testing trans')
trans_options = get_transmissions(trims)
for x in trans_options:
    print(x)
