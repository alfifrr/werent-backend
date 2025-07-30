from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.payment_controller import (
    create_payment_controller,
    get_payment_controller,
    get_all_payments_controller,
    update_payment_controller,
    delete_payment_controller,
    get_payments_by_user_controller
)

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

@payment_bp.before_request
@jwt_required()
def require_jwt():
    pass

# Create a new payment
@payment_bp.route('/', methods=['POST'])
def create_payment():
    current_user_id = get_jwt_identity()
    return create_payment_controller(request.json, current_user_id)

# Get all payments (admin only)
@payment_bp.route('/', methods=['GET'])
def get_all_payments():
    current_user_id = get_jwt_identity()
    return get_all_payments_controller(current_user_id)

# Get a specific payment
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    current_user_id = get_jwt_identity()
    return get_payment_controller(payment_id, current_user_id)

# Update a payment
@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    current_user_id = get_jwt_identity()
    return update_payment_controller(payment_id, request.json, current_user_id)

# Delete a payment
@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    current_user_id = get_jwt_identity()
    return delete_payment_controller(payment_id, current_user_id)

# Get all payments by user_id
@payment_bp.route('/user/<int:user_id>', methods=['GET'])
def get_payments_by_user(user_id):
    current_user_id = get_jwt_identity()
    return get_payments_by_user_controller(user_id, current_user_id) 