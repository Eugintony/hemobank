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

    # Choose config: Render → Production, else Dev/Testing
    if os.getenv("RENDER"):
        config = ProductionConfig
    elif config_name == "testing":
        config = TestingConfig
    else:
        config = DevelopmentConfig

    app.config.from_object(config)

    # Debug print: see exactly which DB your app is using
    print("DB URI IN USE:", app.config["SQLALCHEMY_DATABASE_URI"])

    # Allow all origins – safe for your college project
    CORS(app)

    # Initialize database
    db.init_app(app)

    with app.app_context():
        init_db(app)
        seed_sample_data(app)

    # Register all API blueprints (donors, donations, inventory, etc.)
    register_routes(app)

    # ---------- Page routes (HTML) ----------

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

    # ---------- API routes ----------

    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "database": "PostgreSQL",
            "version": "1.0.0"
        })

    # Aggregated stats for dashboard & inventory
    @app.route("/api/stats")
    def get_stats():
        stats = get_db_stats(app)
        return jsonify(stats)

    @app.route("/api/dashboard/stats")
    def get_dashboard_stats():
        stats = get_db_stats(app)
        return jsonify(stats)

    # ---------- Error handlers ----------

    @app.errorhandler(404)
    def not_found_error(error):
        # For simplicity, return JSON for all 404s
        return jsonify({"error": "Resource not found"}), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
