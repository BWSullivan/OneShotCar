from flask import *
import requests
import json
import os
from werkzeug.utils import secure_filename
import backend_file
import carinfo

def create_app(test_config=None):
    make_name, model_name, years = "", "", ""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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

    path = os.path.join(app.root_path, "static", "uploads" )
    app.config["IMAGE_UPLOADS"] = path
    app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["PNG","JPEG","JPG", "GIF"]

    def allowed_image(filename):
        if not "." in filename:
            return False

        ext = filename.rsplit(".", 1)[1]

        if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
            return True
        else:
            return False
    
    #upload image
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
                    #make_name, model_name, years = main.callAPI(filename)
                    print("Image saved!")

                return redirect(request.url)
        return render_template("index.html")
        

    #automatic page
    @app.route('/')
    def home():
        return render_template("front_page.html")

    #front page
    @app.route('/front_page')
    def front_page():
        return render_template('front_page.html')

    #results page
    @app.route('/results')
    def results():
        make, model, first_year, last_year = carinfo.carnet_ai()
        iprice = carinfo.get_google_result(make, model)

        otherModels = carinfo.get_other_models(make)
        itrims = carinfo.get_trims(make, model, first_year)
        print(itrims)
        itransmissions = carinfo.get_transmissions(make, model, first_year, itrims)
        return render_template('results_page.html', make_name=make, model_name=model, years=first_year, trims=itrims, transmissions=itransmissions, price=iprice, colors='tbc', safety='tbc', engine='tbc', infotainment='tbc', interior='tbc', other_models=otherModels, performance='tbc', safety_features='tbc', interior_features='tbc', comfort_features='tbc', performance_features='tbc')

    #text search page
    @app.route('/search')
    def search():
        return render_template('search.html')
    
    #about us page
    @app.route('/about')
    def about():
        return render_template('about.html')

    #history page
    @app.route('/history')
    def history():
        return render_template('history.html')

    #contact us page
    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    #resources page
    @app.route('/resources')
    def resources():
        return render_template('resources.html')


    return app


#our pages: front page, results page, about us, contact page
#our pages (continued): history, search page, resources page
