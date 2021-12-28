from flask import request, g, Response, jsonify
from flaskapp import app

@app.teardown_appcontext
def close_db(e=None):
    # executed when application context is gone
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def route_main():
    return "hello :)"