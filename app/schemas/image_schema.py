"""
Image schemas for request/response validation.
"""

from typing import Optional, List
from pydantic import Field, HttpUrl, field_validator
from app.schemas.base_schema import BaseSchema, TimestampMixin, ResponseSchema


class ImageCreateSchema(BaseSchema):
    """Schema for creating a new image."""

    url: HttpUrl = Field(..., description="Image URL")
    item_id: int = Field(..., description="ID of the item this image belongs to")
    is_primary: bool = Field(False, description="Whether this is the primary image")

    @field_validator('url')
    @classmethod
    def validate_image_url(cls, v):
        """Validate that URL points to an image."""
        url_str = str(v)
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        if not any(url_str.lower().endswith(ext) for ext in image_extensions):
            raise ValueError('URL must point to an image file')
        return v


class ImageUpdateSchema(BaseSchema):
    """Schema for updating image."""

    is_primary: Optional[bool] = Field(None, description="Whether this is the primary image")


class ImageResponseSchema(BaseSchema, TimestampMixin):
    """Schema for image response."""

    id: int
    url: str
    item_id: int
    is_primary: bool


class ImageListResponseSchema(ResponseSchema):
    """Schema for image list response."""

    images: List[ImageResponseSchema]
    total: int


class ItemImagesResponseSchema(BaseSchema):
    """Schema for all images of an item."""

    item_id: int
    images: List[ImageResponseSchema]
    primary_image: Optional[ImageResponseSchema] = None


class ImageUploadSchema(BaseSchema):
    """Schema for image upload validation."""

    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="File content type")
    size: int = Field(..., description="File size in bytes")

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v):
        """Validate content type is an image."""
        valid_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
        if v not in valid_types:
            raise ValueError(f'Content type must be one of: {valid_types}')
        return v

    @field_validator('size')
    @classmethod
    def validate_file_size(cls, v):
        """Validate file size (max 5MB)."""
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if v > max_size:
            raise ValueError('File size cannot exceed 5MB')
        return v

    @field_validator('filename')
    @classmethod
    def validate_filename(cls, v):
        """Validate filename."""
        if not v.strip():
            raise ValueError('Filename cannot be empty')

        # Check for valid image extension
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        if not any(v.lower().endswith(ext) for ext in image_extensions):
            raise ValueError('Filename must have a valid image extension')

        return v.strip()


class ImageUploadResponseSchema(BaseSchema):
    """Schema for image upload response."""

    success: bool
    message: str
    image_url: Optional[str] = None
    image_id: Optional[int] = None
