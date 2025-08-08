from flask import Flask, g
from blueprints.api import api
from blueprints.frontend import web
from database import init_db
import os

app = Flask(__name__)
app.secret_key = os.urandom(64)

app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = "True"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if not os.path.exists("database.db"):
    with app.app_context():
        init_db()

app.register_blueprint(web, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')

app.run(host='0.0.0.0', port=1337, debug=False, use_evalex=False)