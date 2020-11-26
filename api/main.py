from flask import request, url_for
from flask_cors import CORS, cross_origin
from flask_api import FlaskAPI, status, exceptions

from inverted_index.inverted_index import init_index


app = FlaskAPI(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/search', methods=['POST'])
@cross_origin()
def search_index():
    query = request.data.get('query', None)
    max_results = request.data.get('max_results', 5)
    if query is not None:
        tweets = index.search(max_results, query)
        # TODO: get tweet text
        return {'tweets': tweets}
    return {'error': 'No query provided'}


if __name__ == '__main__':
    global index
    index = init_index()
    app.run(debug=True)
