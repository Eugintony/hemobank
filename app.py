import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models import db
from routes import register_routes
from database import get_db_stats

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    # Detect environment
    if os.getenv("RENDER"):
        config = ProductionConfig()
    elif config_name == "testing":
        config = TestingConfig()
    else:
        config = DevelopmentConfig()

    app.config.from_object(config)

    CORS(app)

    db.init_app(app)

    register_routes(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/dashboard")
    def dashboard():
        return render_template("dashboard.html")

    @app.route("/donors")
    def donors():
        return render_template("donor_list.html")

    @app.route("/donors/register")
    def register_donor_page():
        return render_template("donor_register.html")

    @app.route("/donations/record")
    def record_donation_page():
        return render_template("donation_record.html")

    @app.route("/inventory")
    def inventory_page():
        return render_template("inventory.html")

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "database": "PostgreSQL",
            "version": "1.0.0"
        })

    @app.route("/api/stats")
    def get_stats():
        stats = get_db_stats(app)
        return jsonify(stats)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    return app
