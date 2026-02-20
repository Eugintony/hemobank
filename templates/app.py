import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models import db
from routes import register_routes
from database import init_db, seed_sample_data, get_db_stats

load_dotenv()

def create_app(config_name=None):
    app = Flask(__name__)

    # Auto-detect production on Render
    if os.getenv("RENDER"):
        config = ProductionConfig
    elif config_name == "testing":
        config = TestingConfig
    else:
        config = DevelopmentConfig

    app.config.from_object(config)

    # Allow all origins – safe for your college project
    CORS(app)

    # Initialize database
    db.init_app(app)

    with app.app_context():
        init_db(app)
        seed_sample_data(app)

    # Register API blueprints/routes (donors, donations, inventory, etc.)
    register_routes(app)

    # Frontend routes
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

    # Health check
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "database": "PostgreSQL",
            "version": "1.0.0"
        })

    # Stats for dashboard/inventory (aggregated from Donor + BloodInventory)
    @app.route("/api/stats")
    def get_stats():
        stats = get_db_stats(app)
        return jsonify(stats)

    @app.route("/api/dashboard/stats")
    def get_dashboard_stats():
        # Same data, different URL used by inventory.html and dashboard
        stats = get_db_stats(app)
        return jsonify(stats)

    # 404 JSON handler for API paths
    @app.errorhandler(404)
    def not_found_error(error):
        # For API routes, return JSON; for others, you could render a template if desired
        if str(getattr(error, "description", "")).startswith("/api"):
            return jsonify({"error": "Resource not found"}), 404
        return jsonify({"error": "Resource not found"}), 404

    return app


if __name__ == "__main__":
    app = create_app()
    # Debug True only for local development
    app.run(debug=True)
