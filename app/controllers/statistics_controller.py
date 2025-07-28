from app.services.statistics_service import get_admin_statistics, get_monthly_statistics
from app.utils.responses import success_response, internal_error_response
from flask import request

def get_admin_statistics_controller():
    try:
        stats = get_admin_statistics()
        return success_response("Admin statistics fetched successfully", data=stats)
    except Exception as e:
        # Optionally log the error here
        return internal_error_response(str(e))

def get_monthly_statistics_controller():
    try:
        body = request.get_json()
        year = body.get('year') if body else None
        if not year or not isinstance(year, int):
            return internal_error_response("Missing or invalid 'year' in request body")
        stats = get_monthly_statistics(year)
        return success_response(f"Monthly statistics for {year} fetched successfully", data=stats)
    except Exception as e:
        return internal_error_response(str(e))
