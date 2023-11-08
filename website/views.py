# This file defines where users can navigate to. If you want to add a new page such as login,
# it should be added here

from flask import Blueprint, render_template # Blueprint of application

views = Blueprint('views', __name__) # Define blueprint

# Home page
@views.route('/')
def home():
    return render_template("home.html")

# character page 
@views.route('/characters')
def characters():
    return render_template("characters.html")

# comparisons page
@views.route("/comparisons")
def comparisons():
    return render_template("comparisons.html")

