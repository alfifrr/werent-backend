# Pydantic Schemas Documentation - WeRent Backend

## Overview

Schemas menggunakan Pydantic untuk validasi input/output data di API. Semua schemas menyediakan automatic validation, serialization, dan documentation untuk endpoints.

## Schema Structure

### Base Schemas (`app/schemas/base.py`)

#### `BaseSchema`

Base class untuk semua schemas dengan configuration yang konsisten:

- `from_attributes=True`: Enable ORM mode untuk konversi dari SQLAlchemy models
- `validate_assignment=True`: Validate assignments setelah object creation
- `str_strip_whitespace=True`: Automatically strip whitespace dari strings

#### `TimestampMixin`

Mixin untuk fields timestamp yang umum digunakan:

- `created_at: datetime`

#### `ResponseSchema`

Base response schema dengan fields:

- `success: bool = True`
- `message: Optional[str] = None`

#### `PaginationSchema`

Schema untuk pagination parameters:

- `page: int = 1` (ge=1)
- `limit: int = 20` (ge=1)

#### `PaginatedResponseSchema`

Response schema untuk paginated data:

- `page`, `limit`, `total`, `total_pages`, `has_next`, `has_prev`

## Domain Schemas

### 1. User Schemas (`app/schemas/user.py`)

#### Request Schemas:

- **`UserCreateSchema`**: Membuat user baru

  - Email validation dengan EmailStr
  - Password strength validation (min 8 chars, digit, uppercase)
  - Phone number format validation

- **`UserUpdateSchema`**: Update profile user

  - Optional fields untuk partial updates

- **`UserPasswordUpdateSchema`**: Change password
  - Current password validation
  - New password strength validation
  - Confirm password matching

#### Response Schemas:

- **`UserResponseSchema`**: Basic user data
- **`UserProfileResponseSchema`**: Extended user profile dengan stats
- **`UserListResponseSchema`**: List users dengan pagination

#### Validation Features:

```python
@validator('password')
def validate_password(cls, v):
    if len(v) < 8:
        raise ValueError('Password must be at least 8 characters long')
    if not any(c.isdigit() for c in v):
        raise ValueError('Password must contain at least one digit')
    if not any(c.isupper() for c in v):
        raise ValueError('Password must contain at least one uppercase letter')
    return v
```

### 2. Item Schemas (`app/schemas/item.py`)

#### Request Schemas:

- **`ItemCreateSchema`**: Create item baru

  - Title length validation (3-100 chars)
  - Description length validation (10-1000 chars)
  - Price validation (> 0, max 10,000)

- **`ItemSearchSchema`**: Search dan filter items
  - Price range validation
  - Status validation
  - Category filtering

#### Response Schemas:

- **`ItemResponseSchema`**: Basic item data
- **`ItemDetailResponseSchema`**: Extended dengan owner, images, reviews
- **`ItemAvailabilityResponseSchema`**: Availability check results

#### Advanced Features:

```python
@validator('max_price')
def validate_price_range(cls, v, values):
    if v is not None and 'min_price' in values and values['min_price'] is not None:
        if v < values['min_price']:
            raise ValueError('Maximum price must be greater than minimum price')
    return v
```

### 3. Booking Schemas (`app/schemas/booking.py`)

#### Request Schemas:

- **`BookingCreateSchema`**: Create booking baru

  - Date validation (start date not in past)
  - End date after start date
  - Duration limits (max 30 days)

- **`BookingAvailabilityCheckSchema`**: Check availability
  - Date range validation
  - Exclude specific booking option

#### Response Schemas:

- **`BookingResponseSchema`**: Basic booking data
- **`BookingDetailResponseSchema`**: Extended dengan item dan user data
- **`BookingStatsSchema`**: Booking statistics

#### Date Validation:

```python
@validator('start_date')
def validate_start_date(cls, v):
    if v < date.today():
        raise ValueError('Start date cannot be in the past')
    return v

@validator('end_date')
def validate_end_date(cls, v, values):
    if 'start_date' in values and v <= values['start_date']:
        raise ValueError('End date must be after start date')
    return v
```

### 4. Message Schemas (`app/schemas/message.py`)

#### Request Schemas:

- **`MessageCreateSchema`**: Send message

  - Content length validation (1-1000 chars)
  - Content trimming

- **`MessageMarkReadSchema`**: Bulk mark as read
  - List validation (max 100 messages)

#### Response Schemas:

- **`MessageResponseSchema`**: Basic message data
- **`ConversationResponseSchema`**: Conversation dengan unread count
- **`MessageStatsSchema`**: Message statistics

### 5. Review Schemas (`app/schemas/review.py`)

#### Request Schemas:

- **`ReviewCreateSchema`**: Create review

  - Rating validation (1-5)
  - Comment length validation (min 5 chars)

- **`ReviewSearchSchema`**: Search reviews
  - Rating range validation
  - Content search

#### Response Schemas:

- **`ReviewResponseSchema`**: Basic review data
- **`ReviewStatsSchema`**: Review statistics dengan rating distribution
- **`ReviewRatingDistributionSchema`**: Detailed rating breakdown

#### Rating Validation:

```python
@validator('rating')
def validate_rating(cls, v):
    if v < 1 or v > 5:
        raise ValueError('Rating must be between 1 and 5')
    return v
```

### 6. Image Schemas (`app/schemas/image.py`)

#### Request Schemas:

- **`ImageCreateSchema`**: Add image ke item

  - URL validation dengan HttpUrl
  - Image extension validation

- **`ImageUploadSchema`**: File upload validation
  - File size validation (max 5MB)
  - Content type validation
  - Filename validation

#### Response Schemas:

- **`ImageResponseSchema`**: Basic image data
- **`ItemImagesResponseSchema`**: All images untuk item
- **`ImageUploadResponseSchema`**: Upload result

#### URL Validation:

```python
@validator('url')
def validate_image_url(cls, v):
    url_str = str(v)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    if not any(url_str.lower().endswith(ext) for ext in image_extensions):
        raise ValueError('URL must point to an image file')
    return v
```

### 7. Authentication Schemas (`app/schemas/auth.py`)

#### Request Schemas:

- **`LoginSchema`**: User login
- **`RegisterSchema`**: User registration dengan password confirmation
- **`PasswordResetSchema`**: Password reset dengan token

#### Response Schemas:

- **`LoginResponseSchema`**: Login result dengan tokens
- **`TokenResponseSchema`**: Token data
- **`AuthStatusSchema`**: Authentication status

### 8. Error Schemas (`app/schemas/error.py`)

#### Comprehensive Error Handling:

- **`ErrorSchema`**: Base error schema
- **`ValidationErrorSchema`**: Field validation errors
- **`NotFoundErrorSchema`**: Resource not found
- **`UnauthorizedErrorSchema`**: Authentication required
- **`BusinessLogicErrorSchema`**: Business rule violations

#### Specialized Errors:

- **`BookingErrorSchema`**: Booking-specific errors
- **`ItemUnavailableErrorSchema`**: Item availability errors
- **`RateLimitErrorSchema`**: Rate limiting errors

## Usage Examples

### In Routes:

```python
from app.schemas import UserCreateSchema, UserResponseSchema, ErrorSchema

@app.post("/users", response_model=UserResponseSchema)
async def create_user(user_data: UserCreateSchema):
    try:
        user_service = UserService()
        user = user_service.create_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name,
            phone=user_data.phone
        )
        return UserResponseSchema.from_orm(user)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=ErrorSchema(
                error="validation_error",
                message=str(e)
            ).dict()
        )
```

### Validation in Services:

```python
from app.schemas import BookingCreateSchema

def create_booking_endpoint(booking_data: BookingCreateSchema):
    # Data sudah tervalidasi oleh Pydantic
    # Bisa langsung gunakan booking_data.item_id, etc.
    pass
```

### Response Serialization:

```python
from app.schemas import ItemDetailResponseSchema

def get_item_detail(item_id: int):
    item = item_service.get_by_id(item_id)
    return ItemDetailResponseSchema(
        **item.to_dict(),
        owner=item.owner.to_dict(),
        images=[img.to_dict() for img in item.images],
        reviews_count=len(item.reviews),
        avg_rating=calculate_rating(item.reviews)
    )
```

## Key Features

### 1. **Automatic Validation**

- Type checking
- Range validation
- Format validation
- Custom business rule validation

### 2. **Comprehensive Error Messages**

```python
{
    "success": false,
    "error": "validation_error",
    "message": "Validation failed",
    "field_errors": {
        "email": ["Not a valid email address"],
        "password": ["Password must contain at least one digit"]
    }
}
```

### 3. **ORM Integration**

```python
# Automatic conversion dari SQLAlchemy model
user_response = UserResponseSchema.from_orm(user_model)
```

### 4. **Nested Validation**

```python
class BookingCreateSchema(BaseSchema):
    @validator('end_date')
    def validate_end_date(cls, v, values):
        # Access other fields untuk cross-field validation
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v
```

### 5. **Custom Validators**

```python
@validator('phone')
def validate_phone(cls, v):
    if v is not None:
        cleaned = ''.join(filter(str.isdigit, v))
        if len(cleaned) < 10 or len(cleaned) > 15:
            raise ValueError('Phone number must be between 10-15 digits')
    return v
```

## Benefits

1. **Type Safety**: Automatic type checking dan conversion
2. **Documentation**: Schemas serve sebagai API documentation
3. **Validation**: Comprehensive input validation
4. **Consistency**: Consistent response formats
5. **Developer Experience**: Clear error messages dan auto-completion
6. **Testing**: Easy to test dengan well-defined schemas

## Integration dengan FastAPI

Schemas integrate seamlessly dengan FastAPI untuk:

- Automatic request validation
- Response serialization
- API documentation generation
- Type hints untuk better IDE support

Dengan struktur schemas ini, API menjadi lebih robust, well-documented, dan maintainable.
