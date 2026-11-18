from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///to-do.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False
    app.config["SECRET_KEY"]="super_secret"

    db.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.dash import dash_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    return app