from flask import Blueprint, request, jsonify
from models import db, BloodInventory
from datetime import datetime

bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')

@bp.route('', methods=['GET'])
def get_inventory():
    """Get all blood inventory"""
    inventory = BloodInventory.query.filter_by(status='available').all()
    return jsonify([item.to_dict() for item in inventory])

@bp.route('/<int:inventory_id>', methods=['GET'])
def get_inventory_item(inventory_id):
    """Get specific blood unit"""
    item = BloodInventory.query.get_or_404(inventory_id)
    return jsonify(item.to_dict())

@bp.route('/blood-type/<blood_type>', methods=['GET'])
def get_by_blood_type(blood_type):
    """Get all available units of a specific blood type"""
    inventory = BloodInventory.query.filter_by(
        blood_type=blood_type,
        status='available'
    ).all()
    return jsonify([item.to_dict() for item in inventory])

@bp.route('/use/<int:inventory_id>', methods=['PUT'])
def use_blood_unit(inventory_id):
    """Mark a blood unit as used"""
    try:
        item = BloodInventory.query.get_or_404(inventory_id)
        
        if item.status == 'used':
            return jsonify({'error': 'Blood unit already used'}), 400
        
        if item.status == 'expired':
            return jsonify({'error': 'Cannot use expired blood'}), 400
        
        item.status = 'used'
        item.used_at = datetime.utcnow()
        
        db.session.commit()
        return jsonify({
            'message': 'Blood unit marked as used',
            'inventory': item.to_dict()
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:inventory_id>', methods=['DELETE'])
def delete_inventory(inventory_id):
    """Delete an inventory record"""
    try:
        item = BloodInventory.query.get_or_404(inventory_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Inventory record deleted'}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500