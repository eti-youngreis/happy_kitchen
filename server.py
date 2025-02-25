from flask import Flask
from config import DevelopmentConfig
from create_db import create_db
from extensions import db, login_manager
from controllers.auth_controller import auth_bp
from controllers.recipe_controller import recipe_bp
from controllers.statistics_controller import statistics_bp


def create_app(config_class=DevelopmentConfig):
    create_db(server=config_class.server, database=config_class.database)

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(statistics_bp)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
