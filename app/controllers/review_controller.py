from flask_jwt_extended import get_jwt_identity
from app.services.review_service import ReviewService
from app.schemas.review_schema import ReviewCreateSchema, ReviewUpdateSchema
from app.utils.responses import success_response, error_response, not_found_response, internal_error_response
from app.models.review import Review
from app import db

review_service = ReviewService()

def list_reviews_controller(item_id):
    try:
        reviews = review_service.get_reviews_by_item(item_id)
        data = [review.to_dict() for review in reviews]
        return success_response('Reviews retrieved successfully', data)
    except Exception as e:
        return internal_error_response(str(e))

def create_review_controller(item_id, json_data):
    try:
        schema = ReviewCreateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)
    try:
        user_id = get_jwt_identity()
        review = review_service.create_review(
            item_id=item_id,
            user_id=user_id,
            rating=schema.rating,
            comment=schema.review_message
        )
        return success_response('Review created successfully', review.to_dict(), status_code=201)
    except Exception as e:
        return internal_error_response(str(e))

def update_review_controller(review_id, json_data):
    try:
        schema = ReviewUpdateSchema(**json_data)
    except Exception as e:
        return error_response(f'Invalid input: {str(e)}', status_code=422)
    try:
        user_id = get_jwt_identity()
        review = Review.query.get(review_id)
        if not review:
            return not_found_response('Review')
        if review.user_id != user_id:
            return error_response('You can only update your own reviews', status_code=403)
        updated_review = review_service.update_review(
            review_id=review_id,
            user_id=user_id,
            rating=schema.rating,
            comment=schema.review_message
        )
        return success_response('Review updated successfully', updated_review.to_dict())
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))

def delete_review_controller(review_id):
    try:
        user_id = get_jwt_identity()
        review = Review.query.get(review_id)
        if not review:
            return not_found_response('Review')
        if review.user_id != user_id:
            return error_response('You can only delete your own reviews', status_code=403)
        db.session.delete(review)
        db.session.commit()
        return success_response('Review deleted successfully')
    except Exception as e:
        db.session.rollback()
        return internal_error_response(str(e))
