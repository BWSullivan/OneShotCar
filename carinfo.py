import requests
import random


# returns make, model, years_first, years_last
def carnet_ai():
    # -- Query according to documentation --
    URL_carnet = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'
    query_carnet = {'accept': 'application/json',
                    'api-key': API_KEY_carnet,
                    'Content-Type': 'application/octet-stream'}

    data = open(IMG_DIR, 'rb').read()
    response = requests.post(URL_carnet, headers=query_carnet, data=data)
    try:
        data = response.json()  # parsing json answer
        detection_dict = data['detections']
        if len(detection_dict) > 0:
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

            return make_name, model_name, years_first, years_last, probability
        elif len(detection_dict) == 0:
            return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown"
    except requests.exceptions.RequestException:
        print('error')
        print(response.text)


# returns msrp
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


# returns list of other models
def get_other_models(make_name):  # done
    response_model = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/models/2022/' + make_name
                                      + '?api_token=' + API_KEY_carinfo)

    other_models = response_model.json()  # parsing json answer
    model_list = []
    for model in other_models:
        model_list.append(model['model'])
    return model_list


# returns list of trims
def get_trims(make_name, model_name, years_first):
    response_trim = requests.get(url='https://carmakemodeldb.com/api/v1/car-lists/get/trims/' + years_first + '/'
                                     + make_name + '/' + model_name + '/' + '?api_token=' + API_KEY_carinfo)

    trims_ = response_trim.json()  # parsing json answer
    trim_list = []
    for trim in trims_:
        trim_list.append(trim['trim'])
    return trim_list


# returns list of transmissions
def get_transmissions(make_name, model_name, years_first, list_trims):
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
                if (trans['transmission'] not in list_of_trans) and (trans['transmission'] is not None):
                    list_of_trans.append(trans['transmission'])
            except TypeError:
                print("None found!")
    return list_of_trans


# returns make, model, year, trims formatted for the car_features function (IGNORE)
def carstockpile_api(make_stock, model_stock, years_first):
    # get list of cars from API
    # my goal here is to get the API to maybe work in the best way possible

    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/models'

    years_banned = ['2020', '2021', '2022']  # api only works up to 2019, will pull from the highest year
    if years_first in years_banned:
        years_first = '2019'

    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    list_models = (raw_data['models'])
    string_models = []
    model_stock = model_stock.rstrip()
    for model_chose in list_models:
        if model_chose == model_stock:  # if you found the model, choose it.
            string_models = []
            string_models.append(model_chose)
            break
        if model_chose.find(model) != -1:  # if you don't, append the closest one.
            string_models.append(model_chose)
    best_model = string_models[0]  # index out of range
    # now have the same models as the model found in carnet API

    URL_stockpile = 'https://car-stockpile.p.rapidapi.com/trims'
    response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make, 'model': best_model, 'year': years_first},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    raw_data = response_stockpile.json()
    list_trims = (raw_data['trims'])
    string_trim = []

    for trim in list_trims:
        string_trim.append(trim['trim'])

    final_trim = string_trim[random.randint(0, len(string_trim) - 1)]

    # URL_stockpile = 'https://car-stockpile.p.rapidapi.com/spec-transmission'
    # response_stockpile = requests.get(url=URL_stockpile, params={'make': 'Audi', 'model': 'RS4 Avant', 'year': '2019', 'trim': '2.9 TFSI quattro'}, headers={'X-RapidAPI-Host' : 'car-stockpile.p.rapidapi.com', 'X-RapidAPI-Key' : '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
    # print(response_stockpile.json())

    # we can finally make requests!
    return make, best_model, years_first, final_trim


# returns a list of features depending on option flag
def car_features(make_stock, best_model, years_first, final_trim, option):
    if option == 1:
        URL_stockpile_tire = 'https://car-stockpile.p.rapidapi.com/spec-chassis-wheel'

        response_stockpile = requests.get(url=URL_stockpile_tire,
                                          params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                  'trim': final_trim},
                                          headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                   'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
        raw_data = response_stockpile.json()
        return raw_data

    # -- FEATURES --
    elif option == 2:
        URL_stockpile_features = 'https://car-stockpile.p.rapidapi.com/spec-features'

        response_stockpile = requests.get(url=URL_stockpile_features,
                                          params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                  'trim': final_trim},
                                          headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                   'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
        raw_data = response_stockpile.json()
        return raw_data

    # -- GENERAL SPECS --
    elif option == 3:
        URL_stockpile_general = 'https://car-stockpile.p.rapidapi.com/spec-general'

        response_stockpile = requests.get(url=URL_stockpile_general,
                                          params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                  'trim': final_trim},
                                          headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                   'X-RapidAPI-Key': '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'})
        raw_data = response_stockpile.json()
        return raw_data


# -- KEYS and URLs --

API_KEY_carnet = 'ec8de34a-4d87-44c5-b569-3482f7a12858'

API_KEY_carinfo = 'haOKbNWT5dbmE1SAiFodnUbaMojtX75izMNdChLyulTuo3Ww1reCmA1CqEKR'

API_KEY_google = '4be96181d5e32a353a8cb07555e2d6d85ac7809a90bdbdcbb1ff9cf37ab41968'

API_KEY_stockpile = '0ccc64153emsh2befbe0a2bfcdd1p1ca214jsn646b219efe35'

IMG_DIR = ""

# make
# model
# years_first
# msrp
# other_models_by_make
# all_trims
# all_trans
# tire_list
# feature_list
# general_specs

make, model, years_first, years_last, probability = carnet_ai()
# print(make)
# print(model)
# print(years_first)
# print(years_last)
# print(probability)
msrp = get_google_result(make, model)
#print(msrp)

other_models_by_make = get_other_models(make)
# print('Others: ')
# print(other_models_by_make)

all_trims = get_trims(make, model, years_first)
# print('Trims: ')
# print(all_trims)

all_trans = get_transmissions(make, model, years_first, all_trims)
# print('Trans: ')
# print(all_trans)

# ignore these variables, they're local to carstockpile

new_make, bestmod, caryear, finaltrim = carstockpile_api(make, model, years_first)

tire_list = car_features(new_make, bestmod, caryear, finaltrim, 1)
# print(tire_list)

feature_list = car_features(new_make, bestmod, caryear, finaltrim, 2)
# print(feature_list)

general_specs = car_features(new_make, bestmod, caryear, finaltrim, 3)
# print(general_specs)
