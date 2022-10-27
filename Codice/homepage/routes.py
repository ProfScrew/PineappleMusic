from flask import Blueprint, render_template

from Codice.models import *
from Codice.database import *
from Codice.artist.forms import *

# Blueprint Configuration
homepage = Blueprint('home', __name__, static_folder='static',
                 template_folder='templates')


@homepage.route('/', methods=['GET'])
def home():
    return render_template("index.html", title="Homepage")