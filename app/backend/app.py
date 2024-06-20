from flask import Flask
from flask_cors import CORS
from db import init_db, init_app
from routes.users import users_blueprint
from routes.observations import observations_blueprint
from routes.prediction import prediction_blueprint

def create_app():
    app = Flask(__name__)

    cors_options = {
        "origins": ["http://localhost:5173"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
    }


    app.register_blueprint(users_blueprint, url_prefix="/api/users")
    app.register_blueprint(observations_blueprint, url_prefix="/api/observations")
    app.register_blueprint(prediction_blueprint, url_prefix="/api/predict")

    CORS(app, resources={r"/*": cors_options})

    init_app(app)

    with app.app_context():
        init_db()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
