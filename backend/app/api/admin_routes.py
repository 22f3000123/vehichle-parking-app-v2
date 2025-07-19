from flask import Blueprint, request, jsonify
from flask_security import roles_required
from ..models import ParkingLot, ParkingSpot, db, User, Reservation

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/parking-lots', methods=['POST'])
@roles_required('admin')
def create_parking_lot():
    data = request.get_json()
    new_lot = ParkingLot(
        name=data['name'],
        address=data['address'],
        pincode=data['pincode'],
        number_of_spots=data['number_of_spots'],
        price=data['price']
    )
    db.session.add(new_lot)
    db.session.commit()

    for i in range(new_lot.number_of_spots):
        new_spot = ParkingSpot(lot_id=new_lot.id, spot_number=i + 1)
        db.session.add(new_spot)
    db.session.commit()

    return jsonify({'message': 'Parking lot created successfully'}), 201

@admin_bp.route('/parking-lots', methods=['GET'])
@roles_required('admin')
def get_all_parking_lots_admin():
    parking_lots = ParkingLot.query.all()
    result = []
    for lot in parking_lots:
        result.append({
            'id': lot.id,
            'name': lot.name,
            'address': lot.address,
            'pincode': lot.pincode,
            'number_of_spots': lot.number_of_spots,
            'price': lot.price
        })
    return jsonify(result)

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['GET'])
@roles_required('admin')
def get_parking_lot_details(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    return jsonify({
        'id': lot.id,
        'name': lot.name,
        'address': lot.address,
        'pincode': lot.pincode,
        'number_of_spots': lot.number_of_spots,
        'price': lot.price
    })

@admin_bp.route('/parking-lots/<int:lot_id>/spots', methods=['GET'])
@roles_required('admin')
def get_parking_spots_for_lot(lot_id):
    parking_spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    result = []
    for spot in parking_spots:
        spot_data = {
            'id': spot.id,
            'lot_id': spot.lot_id,
            'spot_number': spot.spot_number,
            'status': spot.status,
            'parking_lot_name': spot.parking_lot.name # Assuming parking_lot relationship is loaded
        }
        if spot.status == 'O':
            reservation = Reservation.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()
            if reservation:
                spot_data['reserved_by'] = {
                    'user_id': reservation.user.id,
                    'email': reservation.user.email,
                    'parking_timestamp': reservation.parking_timestamp.isoformat()
                }
        result.append(spot_data)
    return jsonify(result)

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['PUT'])
@roles_required('admin')
def update_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    data = request.get_json()

    lot.name = data.get('name', lot.name)
    lot.address = data.get('address', lot.address)
    lot.pincode = data.get('pincode', lot.pincode)
    lot.price = data.get('price', lot.price)

    db.session.commit()
    return jsonify({'message': 'Parking lot updated successfully'})

@admin_bp.route('/parking-lots/<int:lot_id>', methods=['DELETE'])
@roles_required('admin')
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)

    if any(spot.status == 'O' for spot in lot.spots):
        return jsonify({'message': 'Cannot delete a lot with occupied spots'}), 400

    ParkingSpot.query.filter_by(lot_id=lot_id).delete()
    db.session.delete(lot)
    db.session.commit()

    return jsonify({'message': 'Parking lot deleted successfully'})

@admin_bp.route('/users', methods=['GET'])
@roles_required('admin')
def get_all_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'active': user.active
    } for user in users])

@admin_bp.route('/parking-spots', methods=['GET'])
@roles_required('admin')
def get_all_parking_spots():
    parking_spots = ParkingSpot.query.all()
    result = []
    for spot in parking_spots:
        spot_data = {
            'id': spot.id,
            'lot_id': spot.lot_id,
            'spot_number': spot.spot_number,
            'status': spot.status,
            'parking_lot_name': spot.parking_lot.name
        }
        if spot.status == 'O':
            reservation = Reservation.query.filter_by(spot_id=spot.id, leaving_timestamp=None).first()
            if reservation:
                spot_data['reserved_by'] = {
                    'user_id': reservation.user.id,
                    'email': reservation.user.email,
                    'parking_timestamp': reservation.parking_timestamp.isoformat()
                }
        result.append(spot_data)
    return jsonify(result)

@admin_bp.route('/summary-charts', methods=['GET'])
@roles_required('admin')
def get_summary_charts_data():
    total_parking_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    occupied_spots = ParkingSpot.query.filter_by(status='O').count()
    total_reservations = Reservation.query.count()

    # Data for parking lot occupancy breakdown
    parking_lot_occupancy = []
    parking_lots = ParkingLot.query.all()
    for lot in parking_lots:
        lot_occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        lot_available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        parking_lot_occupancy.append({
            'lot_id': lot.id,
            'lot_name': lot.name,
            'total_spots': lot.number_of_spots,
            'occupied_spots': lot_occupied_spots,
            'available_spots': lot_available_spots
        })

    return jsonify({
        'total_parking_lots': total_parking_lots,
        'total_spots': total_spots,
        'available_spots': available_spots,
        'occupied_spots': occupied_spots,
        'total_reservations': total_reservations,
        'parking_lot_occupancy': parking_lot_occupancy
    })
