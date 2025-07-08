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



if __name__ == '__main__':
    app.run(debug=True)