import flask
from flask import jsonify
from flask import request
import json
import os
import dataservice

from flask_jwt_extended import create_access_token
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = flask.Flask(__name__,
                  static_url_path='',
                  static_folder='dist')

app.config['JWT_SECRET_KEY'] = "mysecretkey"
jwt = JWTManager(app)

@app.get("/shutdown")
@jwt_required()
def shutdown():
    os._exit(0)

@app.get("/home")
def home():
    return flask.Response(status="200 OK")

@app.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    if dataservice.login(username, password):
        return flask.Response(status=200)

@app.post("/create_account")
def create_account():
    if not login():
        username = request.form["username"]
        password = request.form["password"]
        dataservice.create_account(username,password)
        return flask.Response(status="200 OK",
                              headers={"Content-Type":"application/json"},
                              response=json.dumps(dataservice.get_lists(username)))

@app.get("/lists")
@jwt_required()
def lists():
    username = get_jwt_identity()
    dataservice.get_lists(username)
    return flask.Response(status="200 OK",
                            headers={"Content-Type":"application/json"},
                            response=json.dumps(dataservice.get_lists(username)))

@app.get("/data/<list_name>")
@jwt_required()
def list_data(list_name):
    username = get_jwt_identity()
    dataservice.get_list_data(username, list_name)
    return flask.Response(status="200 OK",
                          headers={"Content-Type":"application/json"},
                          response=json.dumps(dataservice.get_list_data(username, list_name)))

@app.get("/swiss_setup/<list>")
@jwt_required()
def swiss_setup(list):
    username = get_jwt_identity()
    # dataservice.swiss_setup(username, list)
    return flask.Response(status="200 OK",
                          headers={"Content-Type":"application/json"},
                        #   response=json.dumps(dataservice.get_swiss_setup(username, list))
    )

# @app.get("/<path>")
# def catch_all(path):
#     return flask.Response(status="200 OK")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5173)