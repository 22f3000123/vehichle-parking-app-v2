from flask import Blueprint, request, jsonify
from flask_security import roles_required
from datetime import datetime, timedelta
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

    now = datetime.now()
    today = now.date()
    week_ago = today - timedelta(days=7)
    
    # 1. Basic Stat
    parking_lots = ParkingLot.query.all()
    parking_spots = ParkingSpot.query.all()
    reservations = Reservation.query.all()
    
    total_parking_lots = len(parking_lots)
    total_spots = len(parking_spots)
    available_spots = len([s for s in parking_spots if s.status == 'A'])
    occupied_spots = len([s for s in parking_spots if s.status == 'O'])
    total_reservations = len(reservations)
    
    # 2. Time-based Statistics - Daily reservations for the last 7 days
    daily_reservations = {}
    for i in range(7):
        date = today - timedelta(days=i)
        daily_reservations[str(date)] = 0
    
    for res in reservations:
        if res.parking_timestamp.date() >= week_ago:
            date_str = str(res.parking_timestamp.date())
            if date_str in daily_reservations:
                daily_reservations[date_str] += 1
    
    # Convert to list of dicts for JSON serialization
    daily_reservations_list = [{'date': date, 'count': count} 
                             for date, count in daily_reservations.items()]
    
    # 3. Revenue Statistics
    total_revenue = 0
    completed_reservations = [r for r in reservations if r.leaving_timestamp is not None]
    
    # Create a cache for parking spots to avoid N+1 query
    spot_cache = {spot.id: spot for spot in parking_spots}
    
    for res in completed_reservations:
        spot = spot_cache.get(res.spot_id)
        if spot and spot.parking_lot:  # Check if spot and its parking_lot exist
            duration_hours = (res.leaving_timestamp - res.parking_timestamp).total_seconds() / 3600
            total_revenue += spot.parking_lot.price * duration_hours
    
    # 4. Parking Duration Analysis
    durations = []
    for res in completed_reservations:
        duration_hours = (res.leaving_timestamp - res.parking_timestamp).total_seconds() / 3600
        durations.append(duration_hours)
    
    avg_duration = sum(durations) / len(durations) if durations else 0
    
    # 5. Parking Lot Statistics
    parking_lot_stats = []
    
    # Create a mapping of spot_id to parking_lot for faster lookups
    spot_to_lot = {spot.id: spot.parking_lot for spot in parking_spots if hasattr(spot, 'parking_lot')}
    
    for lot in parking_lots:
        lot_spots = [s for s in parking_spots if s.lot_id == lot.id]
        lot_spot_ids = {s.id for s in lot_spots}
        lot_reservations = [r for r in reservations if r.spot_id in lot_spot_ids]
        
        completed_reservations = [r for r in lot_reservations if r.leaving_timestamp is not None]
        completed_reservations_count = len(completed_reservations)
        
        lot_revenue = 0
        for res in completed_reservations:
            duration_hours = (res.leaving_timestamp - res.parking_timestamp).total_seconds() / 3600
            # Get the spot's parking lot to ensure we have the correct price
            spot_lot = spot_to_lot.get(res.spot_id)
            if spot_lot:
                lot_revenue += spot_lot.price * duration_hours
        
        occupied_spots_count = len([s for s in lot_spots if s.status == 'O'])
        available_spots_count = len([s for s in lot_spots if s.status == 'A'])
        occupancy_rate = (occupied_spots_count / len(lot_spots)) * 100 if lot_spots else 0
        
        parking_lot_stats.append({
            'lot_id': lot.id,
            'lot_name': lot.name,
            'total_spots': len(lot_spots),
            'occupied_spots': occupied_spots_count,
            'available_spots': available_spots_count,
            'reservations_count': completed_reservations_count,
            'revenue': round(lot_revenue, 2),
            'occupancy_rate': round(occupancy_rate, 2)
        })
    
    # 6. Reservation Status
    active_reservations = len([r for r in reservations if r.leaving_timestamp is None])
    completed_reservations_count = len(completed_reservations)
    
    return jsonify({
        'total_parking_lots': total_parking_lots,
        'total_spots': total_spots,
        'available_spots': available_spots,
        'occupied_spots': occupied_spots,
        'total_reservations': total_reservations,
        'total_revenue': round(total_revenue, 2),
        'daily_reservations': daily_reservations_list,
        'average_duration_hours': round(avg_duration, 2),
        'reservation_status': {
            'active': active_reservations,
            'completed': completed_reservations_count,
        }
    })
