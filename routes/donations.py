from flask import Blueprint, request, jsonify
from models import db, Donation, Donor, BloodInventory
from datetime import datetime, timedelta

bp = Blueprint("donations", __name__, url_prefix="/api/donations")


@bp.route("", methods=["GET"])
def get_all_donations():
    """Get all donations."""
    try:
        donations = Donation.query.all()
        return jsonify([donation.to_dict() for donation in donations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:donation_id>", methods=["GET"])
def get_donation(donation_id):
    """Get specific donation."""
    try:
        donation = Donation.query.get_or_404(donation_id)
        return jsonify(donation.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 404


@bp.route("/donor/<int:donor_id>", methods=["GET"])
def get_donor_donations(donor_id):
    """Get all donations by a specific donor."""
    try:
        donations = Donation.query.filter_by(donor_id=donor_id).all()
        return jsonify([donation.to_dict() for donation in donations])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/record", methods=["POST"])
def record_donation():
    """Record a new blood donation and add to blood inventory."""
    try:
        data = request.get_json()

        print("Received donation data:", data)  # Debug log

        # Validate required fields
        required_fields = ["donor_id", "donation_date", "quantity_ml", "hemoglobin", "blood_pressure"]
        missing = [field for field in required_fields if field not in data or data[field] is None]

        if missing:
            return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

        # Validate donor exists
        donor = Donor.query.get(data["donor_id"])
        if not donor:
            return jsonify({"error": "Donor not found"}), 404

        # Validate hemoglobin (minimum 12.5)
        if float(data["hemoglobin"]) < 12.5:
            return jsonify({"error": "Hemoglobin must be at least 12.5 g/dL"}), 400

        # Check 90-day rule
        if donor.last_donation:
            days_since = (datetime.utcnow() - donor.last_donation).days
            if days_since < 90:
                return jsonify({
                    "error": f"Donor must wait {90 - days_since} more days before donating"
                }), 400

        # Parse donation date
        donation_date = datetime.strptime(data["donation_date"], "%Y-%m-%d")

        # Create new donation record
        new_donation = Donation(
            donor_id=data["donor_id"],
            donation_date=donation_date,
            quantity_ml=int(data["quantity_ml"]),
            hemoglobin=float(data["hemoglobin"]),
            blood_pressure=data["blood_pressure"],
            notes=data.get("notes", ""),
            recorded_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_donation)
        db.session.flush()  # Get donation ID before creating inventory

        # Add to blood inventory (one unit per donation record)
        expiry_date = donation_date + timedelta(days=35)

        new_inventory = BloodInventory(
            blood_type=donor.blood_type,
            quantity_ml=int(data["quantity_ml"]),
            donation_id=new_donation.id,
            donation_date=donation_date,
            expiry_date=expiry_date,
            status="available",
            added_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        db.session.add(new_inventory)

        # Update donor's last donation date
        donor.last_donation = donation_date
        donor.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            "message": "Donation recorded successfully",
            "donation": new_donation.to_dict()
        }), 201

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        print("Donation error:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500


@bp.route("/<int:donation_id>", methods=["DELETE"])
def delete_donation(donation_id):
    """Delete a donation."""
    try:
        donation = Donation.query.get_or_404(donation_id)
        db.session.delete(donation)
        db.session.commit()
        return jsonify({"message": "Donation deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
