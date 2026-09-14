from flask import Flask, render_template
from flask_cors import CORS

from config.config import DEBUG, HOST, PORT
from routes.extraction_routes import extraction_bp


def create_app():
    """Create and configure the Flask application."""

    app = Flask(__name__)

    # Enable CORS for API requests.
    CORS(app)

    # Register API routes.
    app.register_blueprint(extraction_bp)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )