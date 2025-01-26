from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration (optional)
    # app.config.from_object('config')

    # Import and register the blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app