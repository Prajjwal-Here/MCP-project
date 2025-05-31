from flask import Flask
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Register Blueprints
    from api.pokemon import pokemon_bp
    from api.type_info import type_bp
    from api.compare import compare_bp
    from api.strategy import strategy_bp
    from api.team import team_bp
    from api.nlp import nlp_bp

    app.register_blueprint(pokemon_bp)
    app.register_blueprint(type_bp)
    app.register_blueprint(compare_bp)
    app.register_blueprint(strategy_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(nlp_bp)

    @app.route("/")
    def home():
        return "MCP Server is running!"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)