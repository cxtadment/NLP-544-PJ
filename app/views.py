from flask import Blueprint, render_template, request, jsonify
from app.analyzer.classifiers.classifier_handler import ApiClassifier
from app.analyzer.data_handler import api_microblog_data_handler
from app.models import Hashtag, TestResult, SearchResult
import random

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
    SearchResult.objects.delete()
    keyword = request.args.get('keyword', '莎拉波娃', type=str)
    microblogs = api_microblog_data_handler(keyword)
    random.shuffle(microblogs)
    apiClassifier = ApiClassifier()
    analyze_results = apiClassifier.classify(microblogs)
    SearchResult.objects.insert(analyze_results)

    return jsonify(result=[e.serialize() for e in analyze_results])
