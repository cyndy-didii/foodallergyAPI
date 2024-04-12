from flask import Flask
from flask_jwt_extended import JWTManager
from models.models import db
from config.config import Config
from api.jwt_routes import setup_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt = JWTManager(app)

    setup_routes(app, jwt)

    with app.app_context():
        db.create_all()

    from api.routes import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", debug=True)