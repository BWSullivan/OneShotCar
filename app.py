from flask import *
import requests
import json
import os
from werkzeug.utils import secure_filename
import backend_file

# global variables
pictureSearch = False
textSearch = False

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
        backend_file.user_pic_name = user_pic_name
        return user_pic_name

    @app.route('/index', methods=["GET", "POST"])
    def index():
        pictureSearch = True
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

                return redirect(request.url)
        return render_template("index.html")
        

    #default page
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
        # if pictureSearch == True:
        #     make, model, year = backend_file.get_user_picture()
        # elif textSearch == True:
        #     # engine, trims, other = backend_file.getformhere
        #     # make, model , year = get from search.html
        return render_template('results_page.html', make_name=make, model_name=model, years=year, locations='tbc', colors='tbc', safety='tbc', engine='tbc', infotainment='tbc', interior='tbc', comfort='tbc', performance='tbc', safety_features='tbc', interior_features='tbc', comfort_features='tbc', performance_features='tbc')

    #text search page
    @app.route('/search', methods = ["POST", "GET"])
    def search():
        textSearch = True
        if request.method == "POST":
            user_input_make = request.form['makeInput']
            user_input_model = request.form['makeInput']
            user_input_year = request.form['yearInput']
            return render_template('results_page.html', make_name=user_input_make, model_name=user_input_model, years=user_input_year, locations='tbc', colors='tbc', safety='tbc', engine='tbc', infotainment='tbc', interior='tbc', comfort='tbc', performance='tbc', safety_features='tbc', interior_features='tbc', comfort_features='tbc', performance_features='tbc')
        else:
        # user_input_make, user_input_model, user_input_year = request.args.get('user')
        # user_input_make = requests.args.get('makeInput')
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