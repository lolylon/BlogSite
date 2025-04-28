import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Set session lifetime
    app.permanent_session_lifetime = timedelta(minutes=30)
    
    # Ensure upload directory exists
    os.makedirs(os.path.join(app.root_path, 'static/uploads'), exist_ok=True)
    
    # Register blueprints
    from app.controllers.auth import auth_bp
    from app.controllers.posts import posts_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app