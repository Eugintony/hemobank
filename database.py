from models import db, Donor, Donation, BloodInventory
from datetime import datetime

def init_db(app):
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("✓ Database initialized successfully!")

def seed_sample_data(app):
    """Add sample data for testing"""
    with app.app_context():
        if Donor.query.first() is not None:
            print("✓ Sample data already exists!")
            return
        
        donors = [
            Donor(
                name='Rajesh Kumar',
                age=28,
                email='rajesh@example.com',
                phone='9876543210',
                blood_type='O+',
                address='123 Main St, Mumbai',
                emergency_contact='9876543211'
            ),
            Donor(
                name='Priya Singh',
                age=32,
                email='priya@example.com',
                phone='9876543212',
                blood_type='B+',
                address='456 Park Ave, Delhi',
                emergency_contact='9876543213'
            ),
            Donor(
                name='Amit Patel',
                age=25,
                email='amit@example.com',
                phone='9876543214',
                blood_type='AB+',
                address='789 Oak Rd, Bangalore',
                emergency_contact='9876543215'
            ),
        ]
        
        for donor in donors:
            db.session.add(donor)
        
        db.session.commit()
        print(f"✓ Added {len(donors)} sample donors!")

def get_db_stats(app):
    """Get database statistics for DBMS project"""
    with app.app_context():
        stats = {
            'total_donors': Donor.query.count(),
            'total_donations': Donation.query.count(),
            'total_blood_units': BloodInventory.query.count(),
            'blood_by_type': {},
            'donors_by_blood_type': {}
        }
        
        from sqlalchemy import func
        blood_stats = db.session.query(
            BloodInventory.blood_type,
            func.count(BloodInventory.id).label('count')
        ).group_by(BloodInventory.blood_type).all()
        
        stats['blood_by_type'] = {bt: cnt for bt, cnt in blood_stats}
        
        donor_stats = db.session.query(
            Donor.blood_type,
            func.count(Donor.id).label('count')
        ).group_by(Donor.blood_type).all()
        
        stats['donors_by_blood_type'] = {bt: cnt for bt, cnt in donor_stats}
        
        return stats