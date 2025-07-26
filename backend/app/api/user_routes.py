from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user
from datetime import datetime
import json
import uuid

from ..models import ParkingLot, ParkingSpot, db, Reservation
from ..extensions import redis_client
from ..tasks import export_reservations_as_csv

user_bp = Blueprint("user", __name__)


@user_bp.route("/parking-lots", methods=["GET"])
def get_parking_lots():
    cached_lots = redis_client.get("all_parking_lots")
    if cached_lots:
        return jsonify(json.loads(cached_lots))

    lots = ParkingLot.query.all()
    lots_data = [
        {
            "id": lot.id,
            "name": lot.name,
            "address": lot.address,
            "pincode": lot.pincode,
            "number_of_spots": lot.number_of_spots,
            "price": lot.price,
        }
        for lot in lots
    ]
    redis_client.setex("all_parking_lots", 60, json.dumps(lots_data))
    return jsonify(lots_data)


@user_bp.route("/parking-lots/<int:lot_id>/available-spots", methods=["GET"])
@auth_required()
def get_available_spots(lot_id):
    available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").all()
    return jsonify(
        [
            {"id": spot.id, "spot_number": spot.spot_number, "status": spot.status}
            for spot in available_spots
        ]
    )


@user_bp.route("/parking-lots/<int:lot_id>/book", methods=["POST"])
@auth_required()
def book_parking_spot(lot_id):

    available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status="A").first()
    if not available_spot:
        return jsonify({"message": "No available spots in this parking lot"}), 400

    available_spot.status = "O"
    db.session.add(available_spot)

    new_reservation = Reservation(
        spot_id=available_spot.id,
        user_id=current_user.id,
        parking_timestamp=datetime.now(),
    )
    db.session.add(new_reservation)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Parking spot booked successfully",
                "spot_id": available_spot.id,
                "reservation_id": new_reservation.id,
            }
        ),
        201,
    )


@user_bp.route("/reservations/<int:reservation_id>/release", methods=["POST"])
@auth_required()
def release_parking_spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id != current_user.id:
        return jsonify({"message": "Unauthorized"}), 403

    parking_spot = ParkingSpot.query.get_or_404(reservation.spot_id)
    parking_spot.status = "A"
    db.session.add(parking_spot)

    reservation.leaving_timestamp = datetime.now()
    parking_lot = ParkingLot.query.get(parking_spot.lot_id)
    time_parked_seconds = (
        reservation.leaving_timestamp - reservation.parking_timestamp
    ).total_seconds()
    parking_cost = (time_parked_seconds / 3600) * parking_lot.price  # cost per hour
    reservation.parking_cost = round(parking_cost, 2)
    db.session.add(reservation)
    db.session.commit()

    return jsonify(
        {
            "message": "Parking spot released successfully",
            "parking_cost": reservation.parking_cost,
        }
    )


@user_bp.route("/parking-lots/<int:lot_id>/all-spots", methods=["GET"])
@auth_required()
def get_all_spots(lot_id):
    all_spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    return jsonify(
        [
            {"id": spot.id, "spot_number": spot.spot_number, "status": spot.status}
            for spot in all_spots
        ]
    )


@user_bp.route("/reservations", methods=["GET"])
@auth_required()
def get_user_reservations():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    result = []
    for res in reservations:
        parking_spot = ParkingSpot.query.get(res.spot_id)
        parking_lot_name = ""
        if parking_spot:
            parking_lot = ParkingLot.query.get(parking_spot.lot_id)
            if parking_lot:
                parking_lot_name = parking_lot.name

        result.append(
            {
                "id": res.id,
                "spot_id": res.spot_id,
                "parking_lot_name": parking_lot_name,
                "parking_timestamp": res.parking_timestamp.isoformat(),
                "leaving_timestamp": (
                    res.leaving_timestamp.isoformat() if res.leaving_timestamp else None
                ),
                "parking_cost": res.parking_cost,
            }
        )
    return jsonify(result)


@user_bp.route("/summary-charts", methods=["GET"])
@auth_required()
def get_user_summary_charts_data():
    # Get user's reservations
    user_reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    
    # Separate active and completed reservations
    completed_reservations = [r for r in user_reservations if r.leaving_timestamp is not None]
    active_reservations = [r for r in user_reservations if r.leaving_timestamp is None]
    
    # Calculate basic stats
    total_bookings = len(user_reservations)
    total_amount_spent = sum(r.parking_cost or 0 for r in completed_reservations)
    total_hours_parked = sum(
        (r.leaving_timestamp - r.parking_timestamp).total_seconds() / 3600 
        for r in completed_reservations
    )
    
    # Get parking lot info for most used lot
    lot_usage = {}
    for res in user_reservations:
        spot = ParkingSpot.query.get(res.spot_id)
        if spot:
            lot_id = spot.lot_id
            lot_usage[lot_id] = lot_usage.get(lot_id, 0) + 1
    
    most_used_lot = None
    if lot_usage:
        most_used_lot_id = max(lot_usage, key=lot_usage.get)
        most_used_lot = ParkingLot.query.get(most_used_lot_id).name
    
    # Get current booking details if exists
    current_booking = None
    if active_reservations:
        active = active_reservations[0]  # Assuming only one active booking
        spot = ParkingSpot.query.get(active.spot_id)
        lot = ParkingLot.query.get(spot.lot_id) if spot else None
        current_booking = {
            'spot_number': spot.spot_number if spot else None,
            'lot_name': lot.name if lot else None,
            'start_time': active.parking_timestamp.isoformat(),
            'duration_hours': round((datetime.utcnow() - active.parking_timestamp).total_seconds() / 3600, 2)
        }
    
    return jsonify({
        'current_booking': current_booking,
        'total_amount_spent': round(total_amount_spent, 2),
        'total_hours_parked': round(total_hours_parked, 2),
        'average_booking_duration': round(total_hours_parked / len(completed_reservations), 2) if completed_reservations else 0,
        'favorite_parking_lot': most_used_lot,
        'last_booking': (
            max(r.parking_timestamp for r in completed_reservations).isoformat()
            if completed_reservations else None
        )
    })


@user_bp.route("/payment-datails/<int:res_id>", methods=["GET"])
@auth_required()
def get_payment_data(res_id):

    reservation = Reservation.query.filter_by(id=res_id).first()

    time_parked_seconds = (
        reservation.leaving_timestamp - reservation.parking_timestamp
    ).total_seconds()
    return jsonify({"res_time": time_parked_seconds})


@user_bp.route("/process-payment", methods=["POST"])
@auth_required()
def process_payment():
    data = request.get_json()
    lot_id = data.get("lot_id")
    amount = data.get("amount")

    if not all([lot_id, amount]):
        return jsonify({"message": "Missing lot_id or amount"}), 400

    # random transaction_id
    transaction_id = str(uuid.uuid4())

    user_reservation = Reservation.query.filter_by(user_id=current_user.id).first()

    user_reservation.transaction_id = transaction_id
    user_reservation.payment_status = "success"

    db.session.commit()

    payment_successful = True  # success

    if payment_successful:
        return (
            jsonify(
                {
                    "message": "Payment processed successfully",
                    "transaction_id": transaction_id,
                }
            ),
            200,
        )
    else:
        return jsonify({"message": "Payment failed"}), 400

@user_bp.route("/export-reservations", methods=["POST"])
@auth_required()
def export_reservations():
    export_reservations_as_csv.delay(current_user.id)
    return jsonify({"message": "Your reservation data is being exported and will be sent to your email."}), 202
