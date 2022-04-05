import os

from flask import Flask
from flask import render_template

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

    """# a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'"""

    #front page
    @app.route('/front_page')
    def front_page():
        return render_template('front_page.html')

    #results page
    @app.route('/results')
    def results():
        return render_template('results_page.html', main_features='tbc', locations='tbc', colors='tbc', safety='tbc', engine='tbc', infotainment='tbc', interior='tbc', comfort='tbc', performance='tbc', safety_features='tbc', interior_features='tbc', comfort_features='tbc', performance_features='tbc')

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