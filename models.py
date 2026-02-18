from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid

db = SQLAlchemy()

class Donor(db.Model):
    """Blood Donor Model"""
    __tablename__ = 'donors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True)
    blood_type = db.Column(db.String(3), nullable=False, index=True)
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(15))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_donation = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    donations = db.relationship('Donation', backref='donor', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Donor {self.name} ({self.blood_type})>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'phone': self.phone,
            'blood_type': self.blood_type,
            'address': self.address,
            'emergency_contact': self.emergency_contact,
            'registered_on': self.registered_on.isoformat(),
            'last_donation': self.last_donation.isoformat() if self.last_donation else None,
            'total_donations': len(self.donations),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def can_donate(self):
        """Check if donor can donate (90-day rule)"""
        if not self.last_donation:
            return True
        days_since = (datetime.utcnow() - self.last_donation).days
        return days_since >= 90


class Donation(db.Model):
    """Blood Donation Record"""
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False, index=True)
    donation_date = db.Column(db.DateTime, nullable=False, index=True)
    quantity_ml = db.Column(db.Integer, default=450, nullable=False)
    hemoglobin = db.Column(db.Float, nullable=False)
    blood_pressure = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.Text)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    blood_inventory = db.relationship('BloodInventory', backref='donation_source', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Donation {self.id} - Donor {self.donor_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'donor_id': self.donor_id,
            'donor_name': self.donor.name if self.donor else None,
            'blood_type': self.donor.blood_type if self.donor else None,
            'donation_date': self.donation_date.isoformat(),
            'quantity_ml': self.quantity_ml,
            'hemoglobin': self.hemoglobin,
            'blood_pressure': self.blood_pressure,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class BloodInventory(db.Model):
    """Blood Stock/Inventory"""
    __tablename__ = 'blood_inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    blood_type = db.Column(db.String(3), nullable=False, index=True)
    quantity_ml = db.Column(db.Integer, nullable=False, default=450)
    donation_id = db.Column(db.Integer, db.ForeignKey('donations.id'), nullable=True)
    donation_date = db.Column(db.DateTime, nullable=False, index=True)
    expiry_date = db.Column(db.DateTime, nullable=False, index=True)
    status = db.Column(db.String(20), default='available', index=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    used_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.donation_date and not self.expiry_date:
            self.expiry_date = self.donation_date + timedelta(days=35)
    
    def __repr__(self):
        return f'<BloodInventory {self.blood_type} - {self.quantity_ml}ml>'
    
    def is_expired(self):
        """Check if blood has expired"""
        return datetime.utcnow() > self.expiry_date
    
    def days_until_expiry(self):
        """Get days remaining until expiry"""
        if self.is_expired():
            return 0
        return (self.expiry_date - datetime.utcnow()).days
    
    def to_dict(self):
        return {
            'id': self.id,
            'blood_type': self.blood_type,
            'quantity_ml': self.quantity_ml,
            'donation_id': self.donation_id,
            'donation_date': self.donation_date.isoformat(),
            'expiry_date': self.expiry_date.isoformat(),
            'days_until_expiry': self.days_until_expiry(),
            'status': self.status,
            'is_expired': self.is_expired(),
            'added_at': self.added_at.isoformat(),
            'used_at': self.used_at.isoformat() if self.used_at else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }