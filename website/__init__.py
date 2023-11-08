# This file makes it so that the website folder can be imported

from flask import Flask

# creating application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'JordanThomson StarWars Tech Assement' # encrypt cookies/inception data

    from .views import views

    app.register_blueprint(views, url_prefix='/') # refers to views url prefix

    return app