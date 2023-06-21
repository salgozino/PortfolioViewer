from flask import Flask

from config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.operations import bp as operations_bp
    app.register_blueprint(operations_bp, url_prefix='/operations')

    from app.cash_positions import bp as cash_bp
    app.register_blueprint(cash_bp, url_prefix='/cash')

    return app
