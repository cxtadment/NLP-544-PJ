from flask import Blueprint, render_template
from app.models import Hashtag, TestResult

bp = Blueprint('544pj', __name__)

@bp.route('/')
def index():
    testResults = TestResult.objects
    return render_template("index.html", testResults=testResults)

