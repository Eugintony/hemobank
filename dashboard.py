from flask import Blueprint, jsonify
from models import db, Donor, Donation, BloodInventory
from datetime import datetime, timedelta
from sqlalchemy import func

bp = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')

@bp.route('/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        total_donors = Donor.query.count()
        
        total_donations = Donation.query.count()
        
        available_units = BloodInventory.query.filter_by(status='available').count()
        
        expiry_threshold = datetime.utcnow() + timedelta(days=7)
        expiring_soon = BloodInventory.query.filter(
            BloodInventory.expiry_date <= expiry_threshold,
            BloodInventory.status == 'available'
        ).count()
        
        blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        blood_availability = []
        max_units = 0
        low_stock_types = 0
        
        for blood_type in blood_types:
            count = BloodInventory.query.filter_by(
                blood_type=blood_type,
                status='available'
            ).count()
            
            expiring_count = BloodInventory.query.filter(
                BloodInventory.blood_type == blood_type,
                BloodInventory.expiry_date <= expiry_threshold,
                BloodInventory.status == 'available'
            ).count()
            
            blood_availability.append({
                'blood_type': blood_type,
                'units': count,
                'expiring_units': expiring_count,
                'status': 'critical' if count == 0 else 'low' if count < 5 else 'moderate' if count < 15 else 'good'
            })
            
            max_units = max(max_units, count)
            if count < 5:
                low_stock_types += 1
        
        return jsonify({
            'total_donors': total_donors,
            'total_donations': total_donations,
            'available_units': available_units,
            'expiring_soon': expiring_soon,
            'low_stock_types': low_stock_types,
            'blood_availability': blood_availability,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500