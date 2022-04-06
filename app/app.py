from flask import *
import requests
import json
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

# @app.route("/")
# def index():
#     return render_template('index.html')

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

@app.route("/", methods=["GET", "POST"])
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


if __name__ == "__main__":
    app.run()
