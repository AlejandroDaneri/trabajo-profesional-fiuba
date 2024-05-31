from flask import Flask, jsonify

from flask import Flask
from routes.backtest_routes import backtest_blueprint
from routes.indicator_routes import indicator_blueprint
from config import cache  # Import the cache object from cache.py
app = Flask(__name__)


cache.init_app(app)

app.register_blueprint(backtest_blueprint)
app.register_blueprint(indicator_blueprint)

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'message': error.description}), 500

@app.route('/ping')
def ping():
    return "ok", 200

if __name__ == '__main__':
    app.run()
