from flask import request, Blueprint
from db import query_db, insert_db

observations_blueprint = Blueprint("observations", __name__)

@observations_blueprint.route("/", methods=['POST'])
def save_observation():
    species  = request.json["species"]
    email = request.json["email"]
    location = request.json["location"]
    user_id = query_db(
        "SELECT id FROM users WHERE email=?;",
        [email],
        one=True
    )['id']
    success = insert_db(
        "INSERT INTO observations (species, user_id, location) VALUES (?, ?, ?);",
        [species, user_id, location]
    )
    if success:
        return ({
            "species": request.json["species"],
            "user_id": user_id,
            "location": request.json["location"]
        }, 200)
    return ({"error": "Could not add observation"}, 400)

@observations_blueprint.route("/", methods=['GET'])
def get_all_observations():
    observations = query_db("SELECT * FROM observations")
    if observations:
        return (observations, 200)
    return ({"errpr": "Could not get observations"}, 400)