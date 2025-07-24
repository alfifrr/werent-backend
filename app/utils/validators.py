"""
Input validation utilities for WeRent Backend API.
Provides functions to validate and sanitize various types of input data.
"""

import re
import base64
import io
from typing import Optional, Tuple
try:
    from PIL import Image
except ImportError:
    Image = None


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email format is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email.strip()) is not None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """
    Validate password strength.

    Requirements:
    - At least 8 characters long
    - Contains uppercase letter
    - Contains lowercase letter
    - Contains at least one number

    Args:
        password (str): Password to validate

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    return True, None


def validate_phone(phone: str) -> bool:
    """
    Validate phone number format.
    Accepts various international formats.

    Args:
        phone (str): Phone number to validate

    Returns:
        bool: True if phone format is valid, False otherwise
    """
    if not phone:
        return True  # Phone is optional

    if not isinstance(phone, str):
        return False

    # Remove common separators and spaces
    cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone.strip())

    # Check for valid international phone number format
    # Accepts: +1234567890, 1234567890, +12 345 678 9012, etc.
    pattern = r'^\+?[1-9]\d{6,14}$'
    return re.match(pattern, cleaned_phone) is not None


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, Optional[str]]:
    """
    Validate name fields (first_name, last_name).

    Args:
        name (str): Name to validate
        field_name (str): Field name for error messages

    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not name or not isinstance(name, str):
        return False, f"{field_name} is required"

    name = name.strip()

    if len(name) < 1:
        return False, f"{field_name} cannot be empty"

    if len(name) > 50:
        return False, f"{field_name} cannot exceed 50 characters"

    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r"^[a-zA-Z\s\-']+$", name):
        return False, f"{field_name} can only contain letters, spaces, hyphens, and apostrophes"

    return True, None


def sanitize_string(value: str, max_length: int = None) -> str:
    """
    Sanitize string input by trimming whitespace and optionally limiting length.

    Args:
        value (str): String to sanitize
        max_length (int, optional): Maximum allowed length

    Returns:
        str: Sanitized string
    """
    if not isinstance(value, str):
        return ""

    sanitized = value.strip()

    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length]

    return sanitized


def validate_base64_image(image_str: str) -> bool:
    """
    Validate if a string is a valid base64-encoded image (checks both base64 and image validity).

    Args:
        image_str (str): Base64 string to validate

    Returns:
        bool: True if valid base64 image, False otherwise
    """
    if Image is None:
        return False

    if not image_str or not isinstance(image_str, str):
        return False
    try:
        # Remove data URL prefix if present
        if image_str.startswith('data:image'):
            image_str = image_str.split(',', 1)[-1]
        decoded = base64.b64decode(image_str, validate=True)
        # Try to open as image
        with Image.open(io.BytesIO(decoded)) as img:
            img.verify()  # Will raise if not an image
        return True
    except Exception:
        return False
