from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.payment_service import PaymentService
from app.schemas.payment_schema import PaymentCreate, PaymentUpdate, PaymentOut, PaymentMethod, PaymentType
from app.models.payment import Payment
from pydantic import ValidationError

payment_bp = Blueprint('payment', __name__, url_prefix='/payments')

@payment_bp.before_request
@jwt_required()
def require_jwt():
    pass

# Create payment
@payment_bp.route('/', methods=['POST'])
def create_payment():
    try:
        data = PaymentCreate(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    payment = PaymentService.create_payment(
        booking_id=data.booking_id,
        total_price=data.total_price,
        payment_method=data.payment_method,
        payment_type=data.payment_type,
        user_id=data.user_id
    )
    return jsonify(PaymentOut.from_orm(payment).dict()), 201

# Get all payments
@payment_bp.route('/', methods=['GET'])
def get_payments():
    payments = PaymentService.get_all_payments()
    return jsonify([PaymentOut.from_orm(p).dict() for p in payments]), 200

# Get all payments by user_id
@payment_bp.route('/user/<int:user_id>', methods=['GET'])
def get_payments_by_user(user_id):
    payments = PaymentService.get_payments_by_user_id(user_id)
    return jsonify([PaymentOut.from_orm(p).dict() for p in payments]), 200

# Get payment by id
@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = PaymentService.get_payment(payment_id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify(PaymentOut.from_orm(payment).dict()), 200

# Update payment
@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    try:
        data = PaymentUpdate(**request.json)
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400
    payment = PaymentService.update_payment(payment_id, **data.dict(exclude_unset=True))
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify(PaymentOut.from_orm(payment).dict()), 200

# Delete payment
@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    success = PaymentService.delete_payment(payment_id)
    if not success:
        return jsonify({'error': 'Payment not found'}), 404
    return jsonify({'message': 'Payment deleted'}), 200 