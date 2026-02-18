from flask import Blueprint, request, jsonify
from models import db, Donor
from datetime import datetime, timedelta

bp = Blueprint('donors', __name__, url_prefix='/api/donors')

@bp.route('', methods=['GET'])
def get_all_donors():
    """Get all donors"""
    try:
        donors = Donor.query.all()
        return jsonify([donor.to_dict() for donor in donors])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:donor_id>', methods=['GET'])
def get_donor(donor_id):
    """Get specific donor"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        return jsonify(donor.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/register', methods=['POST'])
def register_donor():
    """Register a new donor"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(k in data for k in ['name', 'age', 'email', 'phone', 'blood_type']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Validate age
        if not (18 <= data['age'] <= 65):
            return jsonify({'error': 'Age must be between 18 and 65'}), 400
        
        # Check if email already exists
        if Donor.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Check if phone already exists
        if Donor.query.filter_by(phone=data['phone']).first():
            return jsonify({'error': 'Phone number already registered'}), 400
        
        # Create new donor
        new_donor = Donor(
            name=data['name'],
            age=data['age'],
            email=data['email'],
            phone=data['phone'],
            blood_type=data['blood_type'],
            address=data.get('address', ''),
            emergency_contact=data.get('emergency_contact', ''),
            registered_on=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_donor)
        db.session.commit()
        
        return jsonify({
            'message': 'Donor registered successfully',
            'donor': new_donor.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    """Update donor information"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        data = request.get_json()
        
        if 'name' in data:
            donor.name = data['name']
        if 'age' in data:
            if not (18 <= data['age'] <= 65):
                return jsonify({'error': 'Age must be between 18 and 65'}), 400
            donor.age = data['age']
        if 'phone' in data:
            donor.phone = data['phone']
        if 'address' in data:
            donor.address = data['address']
        
        donor.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Donor updated successfully',
            'donor': donor.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    """Delete a donor"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        db.session.delete(donor)
        db.session.commit()
        return jsonify({'message': 'Donor deleted successfully'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:donor_id>/can-donate', methods=['GET'])
def can_donate(donor_id):
    """Check if donor can donate (90-day rule)"""
    try:
        donor = Donor.query.get_or_404(donor_id)
        
        if donor.last_donation is None:
            return jsonify({
                'can_donate': True,
                'message': 'Donor can donate'
            })
        
        days_since_last = (datetime.utcnow() - donor.last_donation).days
        
        if days_since_last >= 90:
            return jsonify({
                'can_donate': True,
                'message': 'Donor can donate'
            })
        else:
            days_remaining = 90 - days_since_last
            return jsonify({
                'can_donate': False,
                'message': f'Donor must wait {days_remaining} more days'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500