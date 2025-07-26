"""
Example implementation for file upload approach (future migration)
This demonstrates how to handle multipart file uploads instead of Base64
"""

from flask import request, current_app
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid
from PIL import Image
import io

class ImageUploadService:
    """
    Enhanced image upload service supporting multiple approaches
    """
    
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    PROFILE_IMAGE_SIZE = (400, 400)  # Profile image dimensions
    THUMBNAIL_SIZE = (150, 150)      # Thumbnail dimensions
    
    def __init__(self):
        self.upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads/images')
        os.makedirs(self.upload_folder, exist_ok=True)
    
    def is_allowed_file(self, filename):
        """Check if file extension is allowed."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS
    
    def validate_file_upload(self, file: FileStorage):
        """Validate uploaded file."""
        if file.filename == '':
            raise ValueError("No file selected")
        
        if not self.is_allowed_file(file.filename):
            raise ValueError(f"File type not allowed. Supported: {', '.join(self.ALLOWED_EXTENSIONS)}")
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds {self.MAX_FILE_SIZE // (1024*1024)}MB limit")
        
        return True
    
    def process_profile_image(self, file: FileStorage, user_id: int):
        """
        Process uploaded profile image:
        1. Validate file
        2. Generate unique filename
        3. Resize and optimize
        4. Save multiple versions
        5. Return file paths
        """
        self.validate_file_upload(file)
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"profile_{user_id}_{uuid.uuid4().hex}.{file_extension}"
        
        # Process image with PIL
        image = Image.open(file.stream)
        
        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        
        # Create different sizes
        profile_image = image.copy()
        profile_image.thumbnail(self.PROFILE_IMAGE_SIZE, Image.Resampling.LANCZOS)
        
        thumbnail = image.copy()
        thumbnail.thumbnail(self.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
        
        # Save processed images
        profile_path = os.path.join(self.upload_folder, f"profile_{unique_filename}")
        thumbnail_path = os.path.join(self.upload_folder, f"thumb_{unique_filename}")
        
        # Optimize and save
        profile_image.save(profile_path, optimize=True, quality=85)
        thumbnail.save(thumbnail_path, optimize=True, quality=80)
        
        return {
            'profile_image_path': profile_path,
            'thumbnail_path': thumbnail_path,
            'filename': unique_filename
        }
    
    def upload_to_cloud(self, file_path: str, cloud_folder: str = "profile_images"):
        """
        Upload file to cloud storage (AWS S3, Cloudinary, etc.)
        This is a placeholder for cloud integration
        """
        # Example with boto3 for AWS S3:
        # import boto3
        # s3 = boto3.client('s3')
        # bucket_name = current_app.config['S3_BUCKET']
        # key = f"{cloud_folder}/{os.path.basename(file_path)}"
        # s3.upload_file(file_path, bucket_name, key)
        # return f"https://{bucket_name}.s3.amazonaws.com/{key}"
        
        # For now, return local path
        return f"/static/uploads/{os.path.basename(file_path)}"
    
    def delete_old_images(self, user_id: int):
        """Delete old profile images for a user."""
        import glob
        old_files = glob.glob(os.path.join(self.upload_folder, f"*profile_{user_id}_*"))
        for file_path in old_files:
            try:
                os.remove(file_path)
            except OSError:
                pass  # File already deleted


# Example controller for file upload approach
def upload_profile_image_file(current_user_id):
    """
    Alternative endpoint for file upload (future implementation)
    POST /api/auth/upload-profile-image
    Content-Type: multipart/form-data
    """
    try:
        if 'image' not in request.files:
            return {"error": "No image file provided"}, 400
        
        file = request.files['image']
        image_service = ImageUploadService()
        
        # Process and save image
        result = image_service.process_profile_image(file, current_user_id)
        
        # Upload to cloud (optional)
        profile_url = image_service.upload_to_cloud(result['profile_image_path'])
        thumbnail_url = image_service.upload_to_cloud(result['thumbnail_path'])
        
        # Update user in database
        from app.services.user_service import UserService
        user_service = UserService()
        updated_user = user_service.update_profile(
            user_id=current_user_id,
            profile_image_url=profile_url,
            profile_thumbnail_url=thumbnail_url
        )
        
        return {
            "message": "Profile image updated successfully",
            "data": {
                "profile_image_url": profile_url,
                "thumbnail_url": thumbnail_url,
                "user": updated_user.to_dict()
            }
        }, 200
        
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": "Image upload failed"}, 500


# Frontend JavaScript example for file upload
"""
// Frontend - File Upload Approach
const uploadProfileImage = async (file) => {
    const formData = new FormData();
    formData.append('image', file);
    
    const response = await fetch('/api/auth/upload-profile-image', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            // Don't set Content-Type for FormData - browser sets it automatically
        },
        body: formData
    });
    
    return response.json();
};

// Usage
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        uploadProfileImage(file)
            .then(result => console.log('Upload successful:', result))
            .catch(error => console.error('Upload failed:', error));
    }
};
"""
