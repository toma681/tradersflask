from flask import Flask, json, request, jsonify, session, Response, render_template
from flask_cors import CORS
from flask_cacheify import init_cacheify
import sys

from server.users.cache import cache as users_cache
from server.users.api import users_api
from server.GameB.cache import cache as gameB_cache
from server.GameB.api import gameB_api
from server.GameA.cache import cache as gameA_cache
from server.GameA.api import gameA_api

app = Flask(__name__)
CORS(app)
# users_cache.init_app(app)
# gameB_cache.init_app(app)
# gameA_cache.init_app(app)

cache = init_cacheify(app)

app.register_blueprint(users_api, url_prefix='/users')
app.register_blueprint(gameA_api, url_prefix='/GameA')
app.register_blueprint(gameB_api, url_prefix='/GameB')

app.debug = False # TODO disable
@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
