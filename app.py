from flask import *
import requests
import json
import os
from werkzeug.utils import secure_filename


# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# -- ARGS --
API_KEY = 'ec8de34a-4d87-44c5-b569-3482f7a12858'
URL = 'https://api.carnet.ai/v2/mmg/detect?box_offset=0&box_min_width=180&box_min_height=180&box_min_ratio=1&box_max_ratio=3.15&box_select=center&region=NA'
IMG_DIR = 'backend/test-images/tesla-big.jpg'

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



def create_app(test_config=None):
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
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    print("Image saved!")

                return redirect(request.url)
        return render_template("index.html")

    #front page
    @app.route('/front_page')
    def front_page():
        return render_template('front_page.html')

    #results page
    @app.route('/results')
    def results():
        return render_template('results_page.html', make_name=make_name, model_name=model_name, years=years, locations='tbc', colors='tbc', safety='tbc', engine='tbc', infotainment='tbc', interior='tbc', comfort='tbc', performance='tbc', safety_features='tbc', interior_features='tbc', comfort_features='tbc', performance_features='tbc')

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

"""from flask import Flask
from flask import render_template
#from datetime import datetime*

app = Flask(__name__)

@app.route('/')
def test():
    #current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('base.html',name='nnnnnn', time=1)"""