from flask import request, Blueprint
from db import query_db, insert_db

observations_blueprint = Blueprint("observations", __name__)

@observations_blueprint.route("/", methods=['POST'])
def save_observation():
    species  = request.json["species"]
    username = request.json["username"]
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    user_id = query_db(
        "SELECT id FROM users WHERE username=?;",
        [username],
        one=True
    )['id']
    success = insert_db(
        "INSERT INTO observations (species, user_id, latitude, longitude) VALUES (?, ?, ?, ?);",
        [species, user_id, latitude, longitude]
    )
    if success:
        return ({
            "species": request.json["species"],
            "user_id": user_id,
            "latitude": request.json["latitude"],
            "longitude": request.json["longitude"]
        }, 200)
    return ({"error": "Could not add observation"}, 400)

@observations_blueprint.route("/", methods=['GET'])
def get_all_observations():
    observations = query_db("SELECT * FROM observations")
    if observations:
        return (observations, 200)
    return ({"errpr": "Could not get observations"}, 400)

@observations_blueprint.route("/nearby", methods=['GET'])
def get_nearby_observations():
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    radius = request.json["radius"]
    observations = query_db(
        "SELECT * FROM observations WHERE pow((pow((latitude - ?), 2) + pow((longtitude - ?), 2)), 0.5) < ?",
        [latitude, longitude, radius]
    )

    if observations:
        return (observations, 200)
    return ({"errpr": "Could not get observations"}, 400)