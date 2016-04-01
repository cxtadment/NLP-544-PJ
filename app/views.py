from flask import Blueprint

bp = Blueprint('544pj', __name__)

@bp.route('/')
def index():
    return "This is our 544 project"
