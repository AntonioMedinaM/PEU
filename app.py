from flask import Flask
from views import views

import os

app=Flask(__name__, static_folder='static')
app.register_blueprint(views, url_prefix="/views")

app.secret_key = 'MiCl4v3Pr0v1c10n4l'

#IMG_FOLDER = os.path.join("static", "IMG")

#app.config["UPLOAD_FOLDER"] = IMG_FOLDER


if __name__ == '__main__':
    app.run(debug=True, port=8000)