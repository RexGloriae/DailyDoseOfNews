from flask import Flask, jsonify
from database import Database

app = Flask(__name__)


@app.route('/articles', methods=['GET'])
def articles():
    data = Database().get_all_articles()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)