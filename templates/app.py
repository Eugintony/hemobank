import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import DevelopmentConfig, TestingConfig, ProductionConfig
from models import db
from routes import register_routes
from database import init_db, seed_sample_data, get_db_stats

load_dotenv()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    if config_name == 'testing':
        config = TestingConfig()
    elif config_name == 'production':
        config = ProductionConfig()
    else:
        config = DevelopmentConfig()
    
    app.config.from_object(config)
    
    db.init_app(app)
    CORS(app, origins=config.CORS_ORIGINS)
    
    init_db(app)
    
    with app.app_context():
        seed_sample_data(app)
    
    register_routes(app)
    
    # Serve frontend pages
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/dashboard')
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/donors')
    def donors():
        return render_template('donor_list.html')
    
    @app.route('/donors/register')
    def register_donor_page():
        return render_template('donor_register.html')
    
    @app.route('/donations/record')
    def record_donation_page():
        return render_template('donation_record.html')
    
    @app.route('/inventory')
    def inventory_page():
        return render_template('inventory.html')
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({
            'status': 'healthy',
            'database': 'PostgreSQL',
            'version': '1.0.0'
        })
    
    @app.route('/api/stats', methods=['GET'])
    def get_stats():
        try:
            stats = get_db_stats(app)
            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    
    
    return app

if __name__ == '__main__':
    app = create_app()

    app.run(debug=True, host='0.0.0.0', port=5000)
