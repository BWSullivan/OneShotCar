from flask import *
import requests
import json
import os
from werkzeug.utils import secure_filename
# import backend_file
import carinfo

history_list = []
history_images = []


def create_app(test_config=None):
    make_name, model_name, years = "", "", ""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    server = app.server
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    path = os.path.join(app.root_path, "static", "uploads")
    app.config["IMAGE_UPLOADS"] = path
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG", "JPEG", "JPG", "GIF"]

    def allowed_image(filename):
        if not "." in filename:
            return False

        ext = filename.rsplit(".", 1)[1]

        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False

    # upload image
    def getFilename(image):
        filename = secure_filename(image.filename)
        user_pic_name = os.path.join(app.config["IMAGE_UPLOADS"], filename)
        carinfo.IMG_DIR = user_pic_name
        return user_pic_name

    @app.route('/index', methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            if request.files:
                image = request.files["image"]

                if image.filename == "":
                    print("Image must have a filename.")
                    return redirect(request.url)

                if not allowed_image(image.filename):
                    print("That image extension is not allowed")
                    return redirect(request.url)
                else:
                    filename = getFilename(image)
                    image.save(filename)
                    print("Image saved!")
                return redirect(url_for("results"))
        return render_template("index.html")

    # automatic page
    @app.route('/')
    def home():
        return render_template("front_page.html")

    # front page
    @app.route('/front_page')
    def front_page():
        return render_template('front_page.html')

    @app.route('/pop_up_error')
    def pop_up_error():
        return render_template('pop_up_error.html')

    # results page
    @app.route('/results')
    def results():
        make, model, first_year, last_year, prob = carinfo.carnet_ai()
        this_history = first_year + " " + make + " " + model

        if (make == "Unknown"):
            return render_template('pop_up_error.html')
        else:
            history_list.append(this_history)  # adding to history list

            iprice = carinfo.get_google_result(make, model)
            otherModels = carinfo.get_other_models(make)
            itrims = carinfo.get_trims(make, model, first_year)
            itransmissions = carinfo.get_transmissions(make, model, first_year, itrims)
            my_images = carinfo.google_images(make, model) #UNCOMMENT FOR FINAL WEBSITE
            # my_images = [
            #     'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Maserati_GranTurismo_-_Flickr_-_exfordy_%281%29.jpg/1200px-Maserati_GranTurismo_-_Flickr_-_exfordy_%281%29.jpg',
            #     'https://maserati.scene7.com/is/image/maserati/maserati/international/Models/default/2019/granturismo/versions/granturismo-sport.jpg?$1400x2000$&fit=constrain',
            #     'https://cdn.motor1.com/images/mgl/nOKEG/s1/2022-maserati-granturismo-unofficial-renderings.jpg',
            #     'https://www.motortrend.com/uploads/sites/10/2019/03/2018-maserati-gran-turismo-sport-convertible-angular-front.png']
            history_images.append(my_images[0])

            # carstockpile additional features
            new_make, bestmod, caryear, finaltrim = carinfo.carstockpile_api(make, model, first_year)

            if (new_make != "Unknown"):
                # get and parse tire list
                itire = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 1)
                itire_list = []
                for key in itire:
                    temp_key = key.replace("_", "\n")
                    this_tire = temp_key + ': ' + itire[key]
                    itire_list.append(this_tire.capitalize())

                ifeature = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 2)
                ifeature_list = []
                for key in ifeature:
                    temp_key = key.replace("_", "\n")
                    this_feature = temp_key + ': ' + ifeature[key]
                    ifeature_list.append(this_feature.capitalize())

                igeneral = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 3)
                igeneral_specs = []
                for key in igeneral:
                    temp_key = key.replace("_", "\n")
                    this_gen_spec = temp_key + ': ' + igeneral[key]
                    igeneral_specs.append(this_gen_spec.capitalize())

                iengine = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 4)
                iengine_specs = []
                for key in iengine:
                    temp_key = key.replace("_", "\n")
                    this_engine_spec = temp_key + ': ' + iengine[key]
                    iengine_specs.append(this_engine_spec.capitalize())

                return render_template('results_page.html', make_name=make, model_name=model, years=first_year,
                                       trims=itrims, transmissions=itransmissions, price=iprice, carpictures=my_images,
                                       generalspecs=igeneral_specs, enginespecs=iengine_specs, other_models=otherModels,
                                       featurelist=ifeature_list, tirelist=itire_list)
            else:
                unavailable = []
                unavailable.append("Unavailable Data")
                return render_template('results_page.html', make_name=make, model_name=model, years=first_year,
                                       trims=itrims, transmissions=itransmissions, price=iprice, carpictures=my_images,
                                       generalspecs=unavailable, enginespecs=unavailable, other_models=otherModels,
                                       featurelist=unavailable, tirelist=unavailable)

    # text search page
    @app.route('/search', methods=["POST", "GET"])
    def search():
        if request.method == "POST":
            user_input_make = request.form['makeInput']
            user_input_model = request.form['modelInput']
            user_input_year = request.form['yearInput']

            this_history = user_input_year + " " + user_input_make + " " + user_input_model
            history_list.append(this_history)  # adding to history list

            otherModels = carinfo.get_other_models(user_input_make)

            if len(otherModels) == 0:
                return render_template('pop_up_error.html')
            else:
                iprice = carinfo.get_google_result(user_input_make, user_input_model)
                itrims = carinfo.get_trims(user_input_make, user_input_model, user_input_year)
                itransmissions = carinfo.get_transmissions(user_input_make, user_input_model, user_input_year, itrims)

                my_images = carinfo.google_images(user_input_make, user_input_model)
                # my_images = [
                #     'https://upload.wikimedia.org/wikipedia/commons/thumb/b/bb/Maserati_GranTurismo_-_Flickr_-_exfordy_%281%29.jpg/1200px-Maserati_GranTurismo_-_Flickr_-_exfordy_%281%29.jpg',
                #     'https://maserati.scene7.com/is/image/maserati/maserati/international/Models/default/2019/granturismo/versions/granturismo-sport.jpg?$1400x2000$&fit=constrain',
                #     'https://cdn.motor1.com/images/mgl/nOKEG/s1/2022-maserati-granturismo-unofficial-renderings.jpg',
                #     'https://www.motortrend.com/uploads/sites/10/2019/03/2018-maserati-gran-turismo-sport-convertible-angular-front.png']
                history_images.append(my_images[0])

                # carstockpile additional features
                new_make, bestmod, caryear, finaltrim = carinfo.carstockpile_api(user_input_make, user_input_model,
                                                                                 user_input_year)

                if (new_make != "Unknown"):
                    # get and parse tire list
                    itire = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 1)
                    itire_list = []
                    for key in itire:
                        temp_key = key.replace("_", "\n")
                        this_tire = temp_key + ': ' + itire[key]
                        itire_list.append(this_tire.capitalize())

                    ifeature = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 2)
                    ifeature_list = []
                    for key in ifeature:
                        temp_key = key.replace("_", "\n")
                        this_feature = temp_key + ': ' + ifeature[key]
                        ifeature_list.append(this_feature.capitalize())

                    igeneral = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 3)
                    igeneral_specs = []
                    for key in igeneral:
                        temp_key = key.replace("_", "\n")
                        this_gen_spec = temp_key + ': ' + igeneral[key]
                        igeneral_specs.append(this_gen_spec.capitalize())

                    iengine = carinfo.car_features(new_make, bestmod, caryear, finaltrim, 4)
                    iengine_specs = []
                    for key in iengine:
                        temp_key = key.replace("_", "\n")
                        this_engine_spec = temp_key + ': ' + iengine[key]
                        iengine_specs.append(this_engine_spec.capitalize())

                    return render_template('results_page.html', make_name=user_input_make, model_name=user_input_model,
                                           years=user_input_year, trims=itrims, transmissions=itransmissions,
                                           price=iprice, carpictures=my_images, generalspecs=igeneral_specs,
                                           enginespecs=iengine_specs, other_models=otherModels,
                                           featurelist=ifeature_list, tirelist=itire_list)
                else:
                    unavailable = []
                    unavailable.append("Unavailable Data")
                    return render_template('results_page.html', make_name=user_input_make, model_name=user_input_model,
                                           years=user_input_year, trims=itrims, transmissions=itransmissions,
                                           price=iprice, carpictures=my_images, generalspecs=unavailable,
                                           enginespecs=unavailable, other_models=otherModels,
                                           featurelist=unavailable, tirelist=unavailable)

        else:
            return render_template('search.html')

    # about us page
    @app.route('/about')
    def about():
        return render_template('about.html')

    # history page
    @app.route('/history')
    def history():
        return render_template('history.html', my_history_list=history_list, my_history_images=history_images)

    # contact us page
    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    # resources page
    @app.route('/resources')
    def resources():
        return render_template('resources.html')

    return app

# our pages: front page, results page, about us, contact page
# our pages (continued): history, search page, resources page
