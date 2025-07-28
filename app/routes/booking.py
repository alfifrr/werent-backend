from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.booking_controller import (
    create_booking_controller,
    get_all_bookings_controller,
    get_booking_controller,
    get_bookings_by_user_controller,
    update_booking_controller,
    cancel_booking_controller,
    check_availability_controller,
    get_availability_calendar_controller,
    get_bookings_by_status_controller,
    get_booking_history_controller,
    get_bookings_by_item_controller,
    get_booking_duration_controller,
    get_revenue_controller,
    get_booking_statistics_controller
)

booking_bp = Blueprint('booking', __name__, url_prefix='/bookings')

@booking_bp.before_request
def require_jwt():
    # Allow public access to availability endpoints
    if request.endpoint and 'availability' in request.endpoint:
        return
    # Require JWT for all other endpoints
    jwt_required()(lambda: None)()
    return

# Get bookings (admin: all bookings, regular user: own bookings)
@booking_bp.route('/', methods=['GET'])
def get_bookings():
    current_user_id = get_jwt_identity()
    return get_all_bookings_controller(current_user_id)

# Create a new booking
@booking_bp.route('/', methods=['POST'])
def create_booking():
    current_user_id = get_jwt_identity()
    return create_booking_controller(request.json, current_user_id)

# Check item availability
@booking_bp.route('/availability', methods=['GET'])
def check_availability():
    item_id = request.args.get('item_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    quantity = request.args.get('quantity', type=int)
    return check_availability_controller(item_id, start_date, end_date, quantity)

# Get availability calendar for date range
@booking_bp.route('/availability/calendar', methods=['GET'])
def get_availability_calendar():
    item_id = request.args.get('item_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    return get_availability_calendar_controller(item_id, start_date, end_date)

# Get booking by id
@booking_bp.route('/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    current_user_id = get_jwt_identity()
    return get_booking_controller(booking_id, current_user_id)

# Get all bookings by user_id
@booking_bp.route('/user/<int:user_id>', methods=['GET'])
def get_bookings_by_user(user_id):
    current_user_id = get_jwt_identity()
    return get_bookings_by_user_controller(user_id, current_user_id)

# Update booking (status, dates, etc.)
@booking_bp.route('/<int:booking_id>', methods=['PUT'])
def update_booking(booking_id):
    current_user_id = get_jwt_identity()
    return update_booking_controller(booking_id, request.json, current_user_id)

# Cancel booking - Dedicated endpoint for better UX and security
@booking_bp.route('/<int:booking_id>/cancel', methods=['POST'])
def cancel_booking(booking_id):
    current_user_id = get_jwt_identity()
    return cancel_booking_controller(booking_id, current_user_id)

# Get bookings by status
@booking_bp.route('/status/<status>', methods=['GET'])
def get_bookings_by_status(status):
    current_user_id = get_jwt_identity()
    return get_bookings_by_status_controller(status, current_user_id)

# Get booking history for current user
@booking_bp.route('/history', methods=['GET'])
def get_booking_history():
    current_user_id = get_jwt_identity()
    limit = request.args.get('limit', default=20, type=int)
    return get_booking_history_controller(current_user_id, limit)

# Get bookings for items owned by current user
@booking_bp.route('/item/<int:item_id>', methods=['GET'])
def get_bookings_by_item(item_id):
    current_user_id = get_jwt_identity()
    return get_bookings_by_item_controller(item_id, current_user_id)

# Get booking duration
@booking_bp.route('/<int:booking_id>/duration', methods=['GET'])
def get_booking_duration(booking_id):
    current_user_id = get_jwt_identity()
    return get_booking_duration_controller(booking_id, current_user_id)

# Get revenue statistics for current user's items
@booking_bp.route('/revenue', methods=['GET'])
def get_revenue():
    current_user_id = get_jwt_identity()
    return get_revenue_controller(current_user_id)

# Get booking statistics
@booking_bp.route('/statistics', methods=['GET'])
def get_booking_statistics():
    current_user_id = get_jwt_identity()
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    return get_booking_statistics_controller(start_date_str, end_date_str, current_user_id)
