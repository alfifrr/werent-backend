"""
Response utilities for CamRent Backend API.
Standardizes API response formats and error handling.
"""

from flask import jsonify
from typing import Any, Dict, Optional, Tuple


def success_response(
    message: str, 
    data: Any = None, 
    status_code: int = 200
) -> Tuple[Dict[str, Any], int]:
    """
    Create standardized success response.
    
    Args:
        message (str): Success message
        data (Any, optional): Response data
        status_code (int): HTTP status code (default: 200)
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
        
    return jsonify(response), status_code


def error_response(
    message: str,
    status_code: int = 400,
    error_code: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], int]:
    """
    Create standardized error response.
    
    Args:
        message (str): Error message
        status_code (int): HTTP status code (default: 400)
        error_code (str, optional): Application-specific error code
        details (Dict, optional): Additional error details
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    response = {
        'success': False,
        'error': message
    }
    
    if error_code:
        response['error_code'] = error_code
        
    if details:
        response['details'] = details
        
    return jsonify(response), status_code


def validation_error_response(
    field_errors: Dict[str, str],
    message: str = "Validation failed"
) -> Tuple[Dict[str, Any], int]:
    """
    Create response for validation errors.
    
    Args:
        field_errors (Dict[str, str]): Field-specific error messages
        message (str): General error message
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    return error_response(
        message=message,
        status_code=422,
        error_code="VALIDATION_ERROR",
        details={'field_errors': field_errors}
    )


def not_found_response(resource: str = "Resource") -> Tuple[Dict[str, Any], int]:
    """
    Create standardized 404 response.
    
    Args:
        resource (str): Name of the resource that wasn't found
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    return error_response(
        message=f"{resource} not found",
        status_code=404,
        error_code="NOT_FOUND"
    )


def unauthorized_response(message: str = "Authentication required") -> Tuple[Dict[str, Any], int]:
    """
    Create standardized 401 response.
    
    Args:
        message (str): Unauthorized message
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    return error_response(
        message=message,
        status_code=401,
        error_code="UNAUTHORIZED"
    )


def forbidden_response(message: str = "Access denied") -> Tuple[Dict[str, Any], int]:
    """
    Create standardized 403 response.
    
    Args:
        message (str): Forbidden message
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    return error_response(
        message=message,
        status_code=403,
        error_code="FORBIDDEN"
    )


def internal_error_response(message: str = "Internal server error") -> Tuple[Dict[str, Any], int]:
    """
    Create standardized 500 response.
    
    Args:
        message (str): Error message
        
    Returns:
        Tuple[Dict[str, Any], int]: (response_dict, status_code)
    """
    return error_response(
        message=message,
        status_code=500,
        error_code="INTERNAL_ERROR"
    )
