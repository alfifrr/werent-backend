from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.controllers.review_controller import (
    list_reviews_controller,
    create_review_controller,
    update_review_controller,
    delete_review_controller,
    list_testimonials_controller
)

review_bp = Blueprint('review', __name__, url_prefix='')

# GET /testimonial - List all testimonials (all reviews)
@review_bp.route('/testimonial', methods=['GET'])
def list_testimonials():
    return list_testimonials_controller()

# GET /items/<int:item_id>/reviews - List all reviews for an item
@review_bp.route('/items/<int:item_id>/reviews', methods=['GET'])
def list_reviews(item_id):
    return list_reviews_controller(item_id)

# POST /items/<int:item_id>/reviews - Create a review (user only)
@review_bp.route('/items/<int:item_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(item_id):
    json_data = request.get_json()
    return create_review_controller(item_id, json_data)

# PUT /reviews/<int:review_id> - Edit a review (owner only)
@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    json_data = request.get_json()
    return update_review_controller(review_id, json_data)

# DELETE /reviews/<int:review_id> - Delete a review (owner only)
@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    return delete_review_controller(review_id)
