from flask import Flask, jsonify, request
from database import Database
from resolve import load_articles

app = Flask(__name__)


@app.route('/articles', methods=['GET'])
def articles():
    data = Database().get_all_articles()
    return jsonify(data)

@app.route('/articles/refresh', methods=['POST'])
def refresh():
    try:
        load_articles()
        return jsonify({"status": "ok", "message": "Articles refreshed."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/articles/fill_descriptions', methods=['POST'])
def fill_descriptions():
    try:
        Database().fill_missing_descriptions()
        return jsonify({"status": "ok", "message": "Descriptions updated."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/articles/by_date', methods=['DELETE'])
def delete_by_date():
    data = request.get_json()
    date_to_delete = data.get('date')
    if not date_to_delete:
        return jsonify({"status": "error", "message": "Missing date parameter"}), 400

    try:
        Database().delete_articles_by_date(date_to_delete)
        return jsonify({"status": "ok", "message": f"Articles from {date_to_delete} deleted."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

from flask import request

@app.route('/articles/search', methods=['GET'])
def search():
    q = request.args.get('q', '')
    results = Database().search_articles(q)
    return jsonify(results)

@app.route('/articles/source/<source>', methods=['GET'])
def by_source(source):
    results = Database().get_by_source(source)
    return jsonify(results)

@app.route('/articles/mark_read/<int:article_id>', methods=['POST'])
def mark_read(article_id):
    Database().mark_as_read(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/favorite/<int:article_id>', methods=['POST'])
def mark_favorite(article_id):
    Database().mark_as_favorite(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/favorites', methods=['GET'])
def get_favorites():
    results = Database().get_favorites()
    return jsonify(results)

@app.route('/articles/stats', methods=['GET'])
def get_stats():
    stats = Database().get_stats()
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)