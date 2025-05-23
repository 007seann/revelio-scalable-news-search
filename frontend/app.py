import sys
import os
sys.path.append("./")
sys.path.append("../")
sys.path.append("../backend/indexer/")
sys.path.append("../backend/utils/")
sys.path.append("../backend/search/")
from pathlib import Path
from backend.search.SearchRetriever import SearchRetriever
from backend.indexer.PositionalIndex import PositionalIndex
from backend.utils.VectorSpaceModel import VectorSpaceModel
from flask import Flask, render_template, request

util_dir = Path(os.path.join(os.path.dirname(__file__))).parent.joinpath('utils')
sys.path.append(str(util_dir))

from AppConfig import AppConfig
config = AppConfig()
# from flask_paginate import Pagination, get_page_parameter
app = Flask(__name__)

indexer = PositionalIndex()
# indexer = VectorSpaceModel()
search_retriever = SearchRetriever(indexer)

@app.route('/')
def index():
    return render_template('index.html', results=None)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        query = request.form['query']
        result_cards = search_retriever.get_results(query)
        '''
        for card in result_cards:
            print("Title:", card.title)
            print("Date:", card.date)
            print("Publisher:", card.publisher)
            print("Content:", card.content)
            # Add more attributes as needed
            print("-" * 50)  # Just for visual separation between cards
        '''
        return render_template('search_result.html', query = query, result_cards=result_cards)
    else:
        return "Method not Allowed"


if __name__ == '__main__':
    host = config.get('frontend', 'host')
    port = config.get('frontend', 'port')
    app.run(host=host, debug=True, port=port, use_reloader=False)