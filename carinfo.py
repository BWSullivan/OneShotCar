import requests
import random



IMG_DIR = ""
city = ""
state = ""

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
            if len(mmg) > 0:
                answer_dict = mmg[0]

                make_name = answer_dict['make_name']

                # I have to hardcode stuff to get it through the other API's...
                # this is a temporary solution... this is stupid... Too bad!:
                if make_name == 'Mercedes-Benz':
                    make_name = 'Mercedes'
                if make_name == 'MAZDA':
                    make_name = 'Mazda'

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
            else:
                return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown" #case where API fails
        elif len(detection_dict) == 0:
            return "Unknown", "Unknown", "Unknown", "Unknown", "Unknown" #case where API fails
    except requests.exceptions.RequestException:
        print('error')
        print(response.text)


# returns msrp
def get_google_result(make_name, model_name):
    engine = "google"
    q = make_name + model_name + "MSRP"

    response_google = requests.get(url='https://serpapi.com/search.json'
                                       '?engine=' + engine + '&q=' + q + '&api_key=' + API_KEY_google_3 + '&gl=us')
    googleanswer = response_google.json()
    try:
        knowledge = googleanswer['knowledge_graph']
    except KeyError:
        return "Price not found!"
    try:
        return knowledge['msrp']
    except KeyError:
        return "Price not found!"


# def get_google_locations(make_name, model_name, city):
#     engine = "google"
#     q = make_name + model_name + "near me"
#
#     response_google_location = requests.get(url='https://serpapi.com/locations.json?q=' + city + '&limit=5')
#     location_answer = response_google_location.json()
#     print(location_answer)
#     try:
#         location = location_answer[1]
#         id = location['id']
#         print(id)
#     except KeyError:
#         # print("Location not found")
#         return "Location not found!"

    # response_google = requests.get(url='https://serpapi.com/search.json'
    #     #                                    '?engine=' + engine + '&q=' + q + '&api_key=' + API_KEY_google + '&gl=us')
    #     #
    #     # googleanswer = response_google.json()
    # try:

def get_google_location_websites(make_name, model_name, city, state):
    engine = "google"
    q = make_name+ '+' + model_name+ '+' + "near+me&location="+ city+ "%2C"+state + "%2C+United+States&hl=en&gl=us&google_domain=google.com"
    # print(q)
    response_google_location = requests.get(url='https://serpapi.com/search.json'
                                       + '?q=' + q + '&api_key=' + API_KEY_google_3 )
    location_answer = response_google_location.json()
    # print("location answer: ")
    # print(location_answer)
    try:
        location = location_answer['local_results']
        # print("local_results: ")
        # print(location)
    except KeyError:
        return "Location not found!"
    try:
        places = location['places']
        # print("places: ")
        # print(places)

        results = []
        # results.append(len(places))
        # temp = 0
        for i in range(len(places)):

            loc_details = places[i]
            try:
                loc_name = loc_details['title']
                results.append(loc_name)
                # temp = temp + 1
            except:
                results.append("Data Unavailable")
                continue

            try:
                loc_hours =loc_details['hours']
                results.append(loc_hours)
                # temp = temp + 1

            except:
                results.append("Data Unavailable")
                continue
            try:
                loc_links = loc_details['links']
                loc_web, loc_directions = loc_links['website'], loc_links['directions']
                results.append(loc_web)
                results.append(loc_directions)
                # temp = temp + 2
            except:
                results.append("Data Unavailable")
                results.append("Data Unavailable")
                continue
        # results.append(temp)
        # print("results: ")
        # print(results)
        return results
    except KeyError:
        results = []
        results.append(0)
        results.append("Location not found!")
        results.append(0)
        return results



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
                if trans['transmission'] not in list_of_trans:
                    if trans['transmission'] is None:
                        continue
                    else:
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
                                                'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
    try:
        raw_data = response_stockpile.json()
        list_models = (raw_data['models'])
        string_models = []
        model_stock = model_stock.rstrip()
        for model_chose in list_models:
            if model_chose == model_stock:  # if you found the model, choose it.
                string_models = []
                string_models.append(model_chose)
                break
            if model_chose.find(model_stock) != -1:  # if you don't, append the closest one.
                string_models.append(model_chose)
        best_model = string_models[0]  # index out of range
    # now have the same models as the model found in carnet API

        URL_stockpile = 'https://car-stockpile.p.rapidapi.com/trims'
        response_stockpile = requests.get(url=URL_stockpile,
                                      params={'make': make_stock, 'model': best_model, 'year': years_first},
                                      headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                               'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
        raw_data = response_stockpile.json()

        list_trims = (raw_data['trims'])
        string_trim = []

        for trim in list_trims:
            string_trim.append(trim['trim'])

        final_trim = string_trim[random.randint(0, len(string_trim) - 1)]

    # we can finally make requests!
        return make_stock, best_model, years_first, final_trim
    except (requests.exceptions.JSONDecodeError, TypeError):
        return "Unknown", "Unknown","Unknown","Unknown"
        print('error')
        print(response_stockpile.text)



# returns a list of features depending on option flag
def car_features(make_stock, best_model, years_first, final_trim, option):
    try:
        if option == 1:
            URL_stockpile_tire = 'https://car-stockpile.p.rapidapi.com/spec-chassis-wheel'

            response_stockpile = requests.get(url=URL_stockpile_tire,
                                              params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                      'trim': final_trim},
                                              headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                       'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
            raw_data = response_stockpile.json()
            return raw_data

        # -- FEATURES --
        elif option == 2:
            URL_stockpile_features = 'https://car-stockpile.p.rapidapi.com/spec-features'

            response_stockpile = requests.get(url=URL_stockpile_features,
                                              params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                      'trim': final_trim},
                                              headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                       'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
            raw_data = response_stockpile.json()
            return raw_data

        # -- GENERAL SPECS --
        elif option == 3:
            URL_stockpile_general = 'https://car-stockpile.p.rapidapi.com/spec-general'

            response_stockpile = requests.get(url=URL_stockpile_general,
                                              params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                      'trim': final_trim},
                                              headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                       'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
            raw_data = response_stockpile.json()
            return raw_data

        elif option == 4:
            URL_stockpile_general = 'https://car-stockpile.p.rapidapi.com/spec-fuel-engine'

            response_stockpile = requests.get(url=URL_stockpile_general,
                                              params={'make': make_stock, 'model': best_model, 'year': years_first,
                                                      'trim': final_trim},
                                              headers={'X-RapidAPI-Host': 'car-stockpile.p.rapidapi.com',
                                                       'X-RapidAPI-Key': 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'})
            raw_data = response_stockpile.json()
            return raw_data
    except TypeError:
        print('TypeError')

def google_images(make_name, model_name):
    engine = "google"
    q = make_name + model_name

    response_google = requests.get(url='https://serpapi.com/search.json'
                                       '?engine=' + engine + '&q=' + q + '&api_key=' + API_KEY_google_3 + '&tbm=isch')
    googleanswer = response_google.json()['images_results']
    results = []
    results.append((googleanswer[0])['original'])
    results.append((googleanswer[1])['original'])
    results.append((googleanswer[2])['original'])
    results.append((googleanswer[3])['original'])
    return results



# -- KEYS and URLs --

API_KEY_carnet = 'ec8de34a-4d87-44c5-b569-3482f7a12858'

API_KEY_carinfo = 'haOKbNWT5dbmE1SAiFodnUbaMojtX75izMNdChLyulTuo3Ww1reCmA1CqEKR'

API_KEY_google = '4be96181d5e32a353a8cb07555e2d6d85ac7809a90bdbdcbb1ff9cf37ab41968'

API_KEY_stockpile = 'a0e96a2515mshbc8e69f3ec87373p1b1b61jsn4dc5a4a181f9'

API_KEY_scraper = '465078331accb68e1ddb3184bc3b4a53'

API_KEY_google_2 = '624fbf9642e60b7c2334b345bbce6195d977882a384816c3197e773f60ac2e93'

API_KEY_google_3 = 'fed60ad4c45b95266b082ecd77e7fc361dfbac907dd37c1bf6d23bb0a7416521' #26

API_KEY_google_4 = '565a0c5085ccd3dddd7d8464c2ff4349b9d432d4572693a8ee848df01c53404a' #19

API_KEY_google_5 = '2e9b13dda90f8130fc810aa286e292f7a919ec4df9b3aa2db3739e5e4c21a51b'
# gotWebsites = get_google_location_websites("Toyota", "Camry", "Austin", "Texas")
# print(gotWebsites)


# gotPrice = get_google_result("Toyota", "Camry")
# print(gotPrice)
# -- VARIABLES TO BE USED IN FRONTEND --
#
# make, model, years_first, years_last, probability = carnet_ai()
# #
# msrp = get_google_result(make, model)
# #
# other_models_by_make = get_other_models(make)
# #
# all_trims = get_trims(make, model, years_first)
# #
# all_trans = get_transmissions(make, model, years_first, all_trims)
# #
#
#
#
# # # ignore new_make, bestmod, caryear, finaltrim, they're local to the carfeatures() function
# new_make, bestmod, caryear, finaltrim = carstockpile_api(make, model, years_first)
# #
# tire_list = car_features(new_make, bestmod, caryear, finaltrim, 1)
# #
# feature_list = car_features(new_make, bestmod, caryear, finaltrim, 2)
# #
# general_specs = car_features(new_make, bestmod, caryear, finaltrim, 3)
# #
# engine_specs = car_features(new_make, bestmod, caryear, finaltrim, 4)
# #
# # exterior_images_list = google_images(make, model)
# #
# # # -- DEBUG PRINT STATEMENTS --
# #
# print('Make: ' + make)
# print('Model: ' + model)
# print('Years First: ' + years_first)
# print('Years Last: ' + years_last)
# print('Probability: ')
# print(probability)
# print('MSRP: ' + msrp)
# print('Other models by make: ')
# print(other_models_by_make)
# print('Trims: ')
# print(all_trims)
# print('Trans: ')
# print(all_trans)
# print('Tire Data: ')
# print(tire_list)
# print('Features Data:')
# print(feature_list)
# print('General Data: ')
# print(general_specs)
# print('Engine Data: ')
# print(engine_specs)
# # print('Google Image results: ')
# # print(exterior_images_list)
