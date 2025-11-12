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

@app.post("/login")
def login():
    username = request.form["username"]
    password = request.form["password"]
    if dataservice.login(username, password):
        return flask.Response(status="200 OK")

@app.post("/create_account")
def create_account():
    if not login():
        username = request.form["username"]
        password = request.form["password"]
        dataservice.create_account(username,password)
        return flask.Response(status="200 OK",
                              headers={"Content-Type":"application/json"},
                              response=json.dumps(dataservice.get_lists(username)))

@app.get("/players/<list>")
def get_players(list):
    username = "luke"
    return flask.Response(status="200 OK",
                            headers={"Content-Type":"application/json"},
                            response=json.dumps(dataservice.get_list_data(list)))

@app.get("/lists")
@jwt_required()
def lists():
    username = get_jwt_identity()
    dataservice.get_lists(username)
    return flask.Response(status="200 OK",
                            headers={"Content-Type":"application/json"},
                            response=json.dumps(dataservice.get_lists(username)))

@app.get("/swiss_setup/<list>")
# @jwt_required()
def swiss_setup(list):
    # username = get_jwt_identity()
    data = dataservice.get_list_data(list)
    return flask.Response(status="200 OK",
                        headers={"Content-Type":"application/json"},
                        response=json.dumps(dataservice.get_round_robin_pairings(data, 1)))

@app.get("/rr_next_round/<list>/<round>")
def rr_next_round(list, round):
    data = dataservice.get_list_data(list)
    num_round = int(round)
    return flask.Response(status="200 OK",
                        headers={"Content-Type":"application/json"},
                        response=json.dumps(dataservice.get_round_robin_pairings(data, num_round)))

@app.post("/edit_player/<user_list>")
# @jwt_required()
def add_player(user_list):
    username = "luke"
    player = request.form["player"]
    rating = request.form["rank"]
    dataservice.add_player(username,user_list,player,rating)
    return flask.Response(status="200 OK")

@app.patch("/edit_player/<user_list>")
def edit_player(user_list):
    username = "luke"
    data = request.get_json()
    player = request.form["player"]
    rating = request.form["rank"]
    dataservice.edit_player(username,user_list,player,rating)
    return flask.Response(status="200 OK")

@app.delete("/edit_player/<user_list>")
def delete_player(user_list):
    username = "luke"
    player = request.form["player"]
    dataservice.delete_player(username,user_list,player)
    return flask.Response(status="200 OK") 


@app.get("/elim")
def elim():
    return flask.Response(status="200 OK")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5173)