"""
Image utilities for Base64 handling.
Simple image validation and processing for WeRent Backend.
"""

import base64
import re
from io import BytesIO
from PIL import Image
import imghdr


class ImageValidator:
    """Validates and processes Base64 images."""
    
    # Allowed image formats
    ALLOWED_FORMATS = ['jpeg', 'jpg', 'png', 'webp']
    
    # Maximum file size (5MB in bytes)
    MAX_FILE_SIZE = 5 * 1024 * 1024
    
    # Maximum dimensions
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1920

    @staticmethod
    def validate_base64_image(base64_string):
        """
        Validate Base64 image string.
        
        Args:
            base64_string (str): Base64 encoded image
            
        Returns:
            dict: Validation result with success status and message
        """
        try:
            # Check if it's a valid Base64 string
            if not base64_string:
                return {"success": False, "message": "No image data provided"}
            
            # Remove data URL prefix if present (data:image/jpeg;base64,)
            if base64_string.startswith('data:'):
                base64_string = base64_string.split(',')[1]
            
            # Decode Base64
            try:
                image_data = base64.b64decode(base64_string)
            except Exception:
                return {"success": False, "message": "Invalid Base64 format"}
            
            # Check file size
            if len(image_data) > ImageValidator.MAX_FILE_SIZE:
                size_mb = len(image_data) / (1024 * 1024)
                return {
                    "success": False, 
                    "message": f"Image too large: {size_mb:.1f}MB. Maximum allowed: 5MB"
                }
            
            # Check if it's a valid image
            image_format = imghdr.what(BytesIO(image_data))
            if not image_format or image_format.lower() not in ImageValidator.ALLOWED_FORMATS:
                return {
                    "success": False, 
                    "message": f"Unsupported image format. Allowed: {', '.join(ImageValidator.ALLOWED_FORMATS)}"
                }
            
            # Validate image dimensions using PIL
            try:
                with Image.open(BytesIO(image_data)) as img:
                    width, height = img.size
                    if width > ImageValidator.MAX_WIDTH or height > ImageValidator.MAX_HEIGHT:
                        return {
                            "success": False,
                            "message": f"Image dimensions too large: {width}x{height}. Maximum: {ImageValidator.MAX_WIDTH}x{ImageValidator.MAX_HEIGHT}"
                        }
            except Exception:
                return {"success": False, "message": "Invalid image file"}
            
            return {
                "success": True, 
                "message": "Image validation successful",
                "format": image_format,
                "size_bytes": len(image_data),
                "dimensions": f"{width}x{height}"
            }
            
        except Exception as e:
            return {"success": False, "message": f"Image validation error: {str(e)}"}

    @staticmethod
    def compress_image(base64_string, quality=85, max_width=800):
        """
        Compress and resize Base64 image.
        
        Args:
            base64_string (str): Base64 encoded image
            quality (int): JPEG compression quality (1-100)
            max_width (int): Maximum width for resizing
            
        Returns:
            str: Compressed Base64 image or original if compression fails
        """
        try:
            # Remove data URL prefix if present
            if base64_string.startswith('data:'):
                prefix = base64_string.split(',')[0] + ','
                base64_data = base64_string.split(',')[1]
            else:
                prefix = ''
                base64_data = base64_string
            
            # Decode and open image
            image_data = base64.b64decode(base64_data)
            with Image.open(BytesIO(image_data)) as img:
                # Convert to RGB if necessary (for JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if 'A' in img.mode else None)
                    img = background
                
                # Resize if too large
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_height = int(img.height * ratio)
                    img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                
                # Save as JPEG with compression
                output = BytesIO()
                img.save(output, format='JPEG', quality=quality, optimize=True)
                
                # Encode back to Base64
                compressed_data = base64.b64encode(output.getvalue()).decode('utf-8')
                
                return f"{prefix}{compressed_data}" if prefix else compressed_data
                
        except Exception:
            # Return original if compression fails
            return base64_string
