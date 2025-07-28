from flask import Blueprint
from app.controllers.statistics_controller import get_admin_statistics_controller, get_monthly_statistics_controller
from app.utils.admin_required import admin_required
from flask_jwt_extended import jwt_required

statistics_bp = Blueprint('statistics', __name__, url_prefix='/api/admin/statistics')

@statistics_bp.route('/', methods=['GET'])
@jwt_required()
@admin_required
def admin_statistics():
    return get_admin_statistics_controller()


@statistics_bp.route('/monthly', methods=['POST'])
@jwt_required()
@admin_required
def monthly_statistics():
    return get_monthly_statistics_controller()
