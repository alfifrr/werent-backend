from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.booking_service import BookingService
from app.schemas.booking_schema import BookingCreate, BookingOut
from pydantic import ValidationError
from datetime import date, datetime
from app.utils.admin_required import admin_required
from app.models.user import User

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.before_request
@jwt_required()
def require_jwt():
    pass

# Helper function to check if current user is admin
def is_admin():
    user_id = get_jwt_identity()
    user = User.find_by_id(user_id)
    return user and getattr(user, 'is_admin', False)

# Get all bookings
@booking_bp.route('/', methods=['GET'])
def get_all_bookings():
    bookings = BookingService.get_all_bookings()
    return jsonify([BookingOut.from_orm(b).dict() for b in bookings]), 200

# Create a new booking
@booking_bp.route('/', methods=['POST'])
def create_booking():
    try:
        data = BookingCreate(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    
    user_id = get_jwt_identity()
    booking = BookingService.create_booking(user_id, data.item_id, data.start_date, data.end_date)
    if not booking:
        return jsonify({'error': 'Item not available, not found, or user not verified'}), 400
    return jsonify(BookingOut.from_orm(booking).dict()), 201

# Check item availability
@booking_bp.route('/availability', methods=['GET'])
def check_availability():
    item_id = request.args.get('item_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not (item_id and start_date and end_date):
        return jsonify({'error': 'item_id, start_date, and end_date are required'}), 400
    
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400
    
    available = BookingService.check_availability(item_id, start, end)
    return jsonify({'available': available}), 200

# Get booking by id
@booking_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    user_id = get_jwt_identity()
    booking = BookingService.get_booking(booking_id, user_id if not is_admin() else None)
    if not booking:
        return jsonify({'error': 'Booking not found or access denied'}), 404
    return jsonify(BookingOut.from_orm(booking).dict()), 200

# Get all bookings by user_id
@booking_bp.route('/user/<int:user_id>', methods=['GET'])
def get_bookings_by_user(user_id):
    bookings = BookingService.get_user_bookings(user_id)
    return jsonify([BookingOut.from_orm(b).dict() for b in bookings]), 200

# Update booking (status, dates, etc.)
@booking_bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    user_id = get_jwt_identity()
    data = request.json
    booking = BookingService.get_booking(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    # Only owner or admin can update
    if booking.user_id != user_id and not is_admin():
        return jsonify({'error': 'Access denied'}), 403
    try:
        booking = BookingService.update_booking(booking_id, user_id if not is_admin() else None, **data)
        if not booking:
            return jsonify({'error': 'Booking not found, access denied, or invalid update'}), 404
        return jsonify(BookingOut.from_orm(booking).dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Extend booking
@booking_bp.route('/<int:booking_id>/extend', methods=['POST'])
def extend_booking(booking_id):
    user_id = get_jwt_identity()
    data = request.json
    booking = BookingService.get_booking(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404
    if booking.user_id != user_id and not is_admin():
        return jsonify({'error': 'Access denied'}), 403
    if not data or 'new_end_date' not in data:
        return jsonify({'error': 'new_end_date is required'}), 400
    try:
        new_end_date = date.fromisoformat(data['new_end_date'])
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400
    booking_service = BookingService()
    try:
        booking = booking_service.extend_booking(booking_id, new_end_date, user_id if not is_admin() else None)
        if not booking:
            return jsonify({'error': 'Booking not found or access denied'}), 404
        return jsonify(BookingOut.from_orm(booking).dict()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

# Get bookings by status
@booking_bp.route('/status/<status>', methods=['GET'])
def get_bookings_by_status(status):
    booking_service = BookingService()
    bookings = booking_service.get_bookings_by_status(status)
    return jsonify([BookingOut.from_orm(b).dict() for b in bookings]), 200

# Get booking history for current user
@booking_bp.route('/history', methods=['GET'])
def get_booking_history():
    user_id = get_jwt_identity()
    limit = request.args.get('limit', default=20, type=int)
    booking_service = BookingService()
    bookings = booking_service.get_booking_history(user_id, limit)
    return jsonify([BookingOut.from_orm(b).dict() for b in bookings]), 200

# Get bookings for items owned by current user
@booking_bp.route('/item/<int:item_id>', methods=['GET'])
def get_bookings_by_item(item_id):
    # Note: You might want to add authorization check to ensure user owns the item
    booking_service = BookingService()
    bookings = booking_service.get_bookings_by_item(item_id)
    return jsonify([BookingOut.from_orm(b).dict() for b in bookings]), 200

# Get booking duration
@booking_bp.route('/<int:booking_id>/duration', methods=['GET'])
def get_booking_duration(booking_id):
    user_id = get_jwt_identity()
    booking = BookingService.get_booking(booking_id, user_id if not is_admin() else None)
    if not booking:
        return jsonify({'error': 'Booking not found or access denied'}), 404
    
    booking_service = BookingService()
    duration = booking_service.calculate_duration_days(booking_id)
    return jsonify({'duration_days': duration}), 200

# Get revenue statistics for current user's items
@booking_bp.route('/revenue', methods=['GET'])
def get_revenue():
    user_id = get_jwt_identity()
    booking_service = BookingService()
    total_revenue = booking_service.calculate_total_revenue(user_id)
    return jsonify({'total_revenue': total_revenue}), 200

# Get booking statistics
@booking_bp.route('/statistics', methods=['GET'])
def get_booking_statistics():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    start_date = None
    end_date = None
    
    if start_date_str:
        try:
            start_date = datetime.fromisoformat(start_date_str)
        except ValueError:
            return jsonify({'error': 'Invalid start_date format, use YYYY-MM-DD'}), 400
    
    if end_date_str:
        try:
            end_date = datetime.fromisoformat(end_date_str)
        except ValueError:
            return jsonify({'error': 'Invalid end_date format, use YYYY-MM-DD'}), 400
    
    booking_service = BookingService()
    stats = booking_service.get_booking_statistics(start_date, end_date)
    return jsonify(stats), 200
