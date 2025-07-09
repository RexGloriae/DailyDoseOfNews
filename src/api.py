from flask import Flask, jsonify, request
from database import Database
from resolve import load_articles
from logs import *

app = Flask(__name__)


@app.route('/articles', methods=['GET'])
def articles():
    data = Database().get_all_articles()
    return jsonify(data)

@app.route('/articles/load', methods=['POST'])
def load():
    try:
        load_articles()
        return jsonify({"status": "ok", "message": "Articles loaded..."})
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
    print(f"[SEARCH] Searching for an article with the keyword: {q}...")
    logging.info(f"Searching for an article with the keyword: {q}...")
    results = Database().search_articles(q)
    if results is None:
        results = []
        print("[SEARCH] No result was found...")
        logging.warning("No result was found...")
    else:
        print("[SEARCH] Found matching article...")
        logging.info("Found matching article...")
    return jsonify(results)

@app.route('/articles/source/<source>', methods=['GET'])
def by_source(source):
    print(f"[SEARCH] Searching all articles from: {source}...")
    logging.info(f"Searching all articles from: {source}...")
    results = Database().get_by_src(source)
    if results is None:
        results = []
        print("[SEARCH] No articles were found...")
        logging.warning("No articles were found...")
    return jsonify(results)

@app.route('/articles/mark_read/<int:article_id>', methods=['POST'])
def mark_read(article_id):
    print(f"[INFO] Marking as read article with id: {article_id}")
    logging.info(f"Marking as read article with id: {article_id}")
    Database().mark_as_read(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/favorite/<int:article_id>', methods=['POST'])
def mark_favorite(article_id):
    print(f"[INFO] Marking as favorite article with id: {article_id}")
    logging.info(f"Marking as favorite article with id: {article_id}")
    Database().mark_as_favorite(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/unmark_read/<int:article_id>', methods=['POST'])
def unmark_read(article_id):
    print(f"[INFO] Marking as not read article with id: {article_id}")
    logging.info(f"Marking as not read article with id: {article_id}")
    Database().unmark_as_read(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/unfavorite/<int:article_id>', methods=['POST'])
def unmark_favorite(article_id):
    print(f"[INFO] Removing as favorite article with id: {article_id}")
    logging.info(f"Removing as favorite article with id: {article_id}")
    Database().unmark_as_favorite(article_id)
    return jsonify({"status": "ok"})

@app.route('/articles/favorites', methods=['GET'])
def get_favorites():
    print("[SEARCH] Searching for favorite articles...")
    logging.info("Searching for favorite articles...")
    results = Database().get_favorites()
    if results is None:
        results = []
        print("[SEARCH] No favorite article was found...")
        logging.warning("No favorite article was found...")
    else:
        print("[SEARCH] Found favorite articles...")
        logging.info("Found favorite articles...")
    return jsonify(results)

@app.route('/articles/stats', methods=['GET'])
def get_stats():
    print("[INFO] Getting statistics...")
    logging.info("Getting statistics...")
    stats = Database().get_stats()
    if stats is None:
        stats = []
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True)