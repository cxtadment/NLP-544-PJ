from flask import Blueprint, render_template
from app.models import Hashtag

bp = Blueprint('544pj', __name__)

@bp.route('/')
def index():
    hashtags = Hashtag.objects
    return render_template("index.html", hashtags=hashtags)

