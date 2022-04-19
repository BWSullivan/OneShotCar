import requests
import random


def carnet_ai():
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
        return make_name, model_name, years

    except requests.exceptions.RequestException:
        print('error')
        print(response.text)


def get_google_result(make_name, model_name):
    engine = "google"
    q = make_name + model_name + "MSRP"

    response_google = requests.get(url='https://serpapi.com/search.json'
                                       '?engine=' + engine + '&q=' + q + '&api_key=' + API_KEY_google)
    googleanswer = response_google.json()
    # print(googleanswer['knowledge_graph'])
    try:
        knowledge = googleanswer['knowledge_graph']
    except KeyError:
        return "MSRP not found!"
    try:
        return knowledge['msrp']
    except KeyError:
        return "MSRP not found!"


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


def get_transmissions(list_trims):
    # O(n^2) avg case, this takes forever. Not sure if there is another way
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


def ninja_api():
    make = 'honda'
    model = 'civic'
    year = 2018
    api_url = 'https://api.api-ninjas.com/v1/cars?make=tesla?year=2012'
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY_ninja})
    data = response.json()
    for x in data:
        print(x)


def shine_api():
    API_KEY_shine = 'VvmCH4l92hEhgIZfA3LC9KLAsnXkHhm1'
    consumer_secret = 'PaePrepDBpI5xMMe'
    response = requests.get(url='https://apis.solarialabs.com/shine/v1/vehicle-stats/specs?make=Honda&model=Civic&year=2016&full-data=True&apikey=' + API_KEY_shine)
    print(response.text)


def carstockpile_api(make_stock, model_stock, years_first):

    # get list of cars from API
    # my goal here is to get the API to maybe work in the best way possible
    multiple_models = False

    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/models'

    years_banned = ['2020', '2021', '2022']  # api only works up to 2019, will pull from the highest year
    if years_first in years_banned:
        years_first = '2019'


    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key' : '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    list_models = (raw_data['models'])
    string_models = []
    for model_chose in list_models:
        if model_chose == model_stock:  # if you found the model, choose it.
            string_models = []
            string_models.append(model_chose)
            multiple_models = False
            break
        if model_chose.find(model) != -1:  # if you don't, append the closest one.
            string_models.append(model_chose)
            multiple_models = True

    best_model = string_models[0]
    # now have the same models as the model found in carnet API


    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/trims'

    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make, 'model': best_model, 'year': years_first},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key' : '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    list_trims = (raw_data['trims'])
    string_trim = []

    for trim in list_trims:
        string_trim.append(trim['trim'])

    final_trim = string_trim[random.randint(0, len(string_trim))]
    print(final_trim)

    # URL_stockpile = 'https://car-stockpile.p.rapidapi.com/spec-transmission'
    # response_stockpile = requests.get(url=URL_stockpile, params={'make': 'Audi', 'model': 'RS4 Avant', 'year': '2019', 'trim': '2.9 TFSI quattro'}, headers={'X-RapidAPI-Host' : 'car-stockpile.p.rapidapi.com', 'X-RapidAPI-Key' : '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    # print(response_stockpile.json())

    # we can finally make requests!

    # -- TIRE SIZES --
    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/spec-chassis-wheel'

    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock, 'model': best_model, 'year': years_first, 'trim': final_trim},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    print(raw_data)

    # -- FEATURES --
    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/spec-features'

    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock, 'model': best_model, 'year': years_first, 'trim': final_trim},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    print(raw_data)

    # --
    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/spec-general'

    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock, 'model': best_model, 'year': years_first, 'trim': final_trim},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    print(raw_data)



def carquery_api():
    response_carquery = requests.get(url='https://www.carqueryapi.com/api/0.3/?callback=?&cmd=getMakes&year=2000&sold_in_us=1', headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'})
    print(response_carquery.content.decode())


# -- KEYS and URLs --
API_KEY_carnet = 'ec8de34a-4d87-44c5-b569-3482f7a12858'
URL_carnet = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'

API_KEY_carinfo = 'haOKbNWT5dbmE1SAiFodnUbaMojtX75izMNdChLyulTuo3Ww1reCmA1CqEKR'
# HERE IS IMG
IMG_DIR = 'comp.jpg'

API_KEY_google = '4be96181d5e32a353a8cb07555e2d6d85ac7809a90bdbdcbb1ff9cf37ab41968'

API_KEY_ninja = 'nX781Gfb0tmE9iL1U2vFZw==zvSlYp1cdKH8M3qk'

API_KEY_stockpile = '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'

API_KEY_carsxe = 'vy7h9rr8c_igmdxi7as_v7krx6teu'


# -- TEST AREA --

# - CARNET.AI

print("")
make, model, years = carnet_ai()
print(make)
print(model)
print(years)
years_list = years.split('-')
years_first = years_list[0]
years_last = years_list[1]
for x in years_list:
    print(x)

# print(get_google_result(make, model))

# print("")
# print('Testing other models')
# other_models_today = get_other_models()
# for x in other_models_today:
#    print(x)

# print("")
# print('Testing trims')
# trims = get_trims()
# for x in trims:
#    print(x)

# this takes way too long
# print("")
# print('Testing trans')
# trans_options = get_transmissions(trims)
# for x in trans_options:
#    print(x)


# msrp = get_google_result()

# ninja_api()
# shine_api()


carstockpile_api(make, model, years_first)
get_google_result(make, model)

# -- CAR STOCKPILE --













# carquery_api()