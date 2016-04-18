from flask import Blueprint, render_template, request, jsonify
from app.analyzer.classifiers.classifier_handler import ApiClassifier
from app.analyzer.data_handler import api_microblog_data_handler
from app.models import Hashtag, TestResult

bp = Blueprint('544pj', __name__)

@bp.route('/')
def index():
    testResults = TestResult.objects
    return render_template("index.html", testResults=testResults)

@bp.route('/search')
def search():
    return render_template("search.html")

@bp.route('/futurework')
def futurework():
    return render_template("futurework.html")

@bp.route('/team')
def team():
    return render_template("team.html")


@bp.route('/searchApi')
def analyze_microblogs_from_api():
    keyword = request.args.get('keyword', '莎拉波娃', type=str)
    microblogs = api_microblog_data_handler(keyword)
    apiClassifier = ApiClassifier()
    analyze_results = apiClassifier.classify(microblogs)
    print(len(analyze_results))
    return jsonify(analyze_results)
