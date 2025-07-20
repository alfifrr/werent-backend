# Services Architecture - WeRent Backend

## Overview

Business logic telah dipisahkan dari models ke dalam services yang terpisah. Models sekarang hanya berisi database fields, relationships, dan basic data conversion methods. Semua business logic dipindahkan ke services.

## Service Structure

### Base Service (`app/services/base_service.py`)

**Purpose**: Menyediakan common CRUD operations untuk semua services

**Methods**:

- `save(instance)`: Save instance ke database
- `delete(instance)`: Delete instance dari database
- `get_by_id(id)`: Get instance by ID
- `get_all()`: Get semua instances
- `create(**kwargs)`: Create instance baru
- `update(instance, **kwargs)`: Update instance
- `delete_by_id(id)`: Delete by ID

### User Service (`app/services/user_service.py`)

**Purpose**: Handle user authentication, profile management, dan user operations

**Key Methods**:

- `create_user(email, password, name, phone)`: Create user baru dengan hashed password
- `authenticate_user(email, password)`: Authenticate user
- `find_by_email(email)`: Find user by email
- `verify_user(user_id)`: Verify user account
- `update_password(user_id, new_password)`: Update password
- `update_profile(user_id, **kwargs)`: Update profile
- `calculate_user_rating(user_id)`: Calculate avg rating dari items
- `get_user_stats(user_id)`: Get user statistics
- `search_users(query)`: Search users
- `check_email_exists(email)`: Check email availability

### Item Service (`app/services/item_service.py`)

**Purpose**: Handle item management, availability, dan item operations

**Key Methods**:

- `create_item(title, description, price_per_day, category, owner_id)`: Create item baru
- `get_available_items()`: Get semua available items
- `get_items_by_owner(owner_id)`: Get items by owner
- `search_items(query)`: Search items by title/description
- `update_item_status(item_id, status)`: Update item status
- `mark_as_rented/available/maintenance(item_id)`: Status management
- `calculate_item_rating(item_id)`: Calculate item rating
- `get_popular_items(limit)`: Get popular items
- `get_top_rated_items(limit)`: Get top rated items
- `filter_items(category, min_price, max_price, status)`: Filter items
- `get_item_availability_calendar(item_id, start_date, end_date)`: Check availability

### Booking Service (`app/services/booking_service.py`)

**Purpose**: Handle booking management, availability checking, dan booking operations

**Key Methods**:

- `create_booking(item_id, renter_id, start_date, end_date)`: Create booking dengan validation
- `is_available_for_dates(item_id, start_date, end_date)`: Check availability
- `confirm_booking(booking_id)`: Confirm pending booking
- `complete_booking(booking_id)`: Mark booking as completed
- `cancel_booking(booking_id)`: Cancel booking
- `get_bookings_by_renter/item/status()`: Get bookings by criteria
- `get_active_bookings()`: Get currently active bookings
- `get_upcoming_bookings(days_ahead)`: Get upcoming bookings
- `calculate_total_revenue(owner_id)`: Calculate revenue
- `extend_booking(booking_id, new_end_date)`: Extend booking

### Message Service (`app/services/message_service.py`)

**Purpose**: Handle messaging between users dan conversation management

**Key Methods**:

- `send_message(sender_id, receiver_id, content)`: Send message
- `get_conversation(user1_id, user2_id, limit)`: Get conversation
- `get_user_conversations(user_id)`: Get all conversations for user
- `mark_conversation_as_read(user_id, partner_id)`: Mark messages as read
- `get_unread_messages/count(receiver_id)`: Get unread messages
- `search_messages(user_id, query)`: Search messages
- `get_message_statistics(user_id)`: Get message stats
- `validate_message_content(content)`: Validate message

### Review Service (`app/services/review_service.py`)

**Purpose**: Handle reviews dan ratings untuk items

**Key Methods**:

- `create_review(item_id, user_id, rating, comment)`: Create review dengan validation
- `update_review(review_id, user_id, rating, comment)`: Update review
- `delete_review(review_id, user_id)`: Delete review
- `get_reviews_by_item/user(id)`: Get reviews by criteria
- `get_item_average_rating(item_id)`: Calculate item rating
- `can_user_review_item(user_id, item_id)`: Check if user can review
- `get_review_statistics(item_id/user_id)`: Get review stats
- `update_owner_rating(owner_id)`: Update owner avg rating

### Image Service (`app/services/image_service.py`)

**Purpose**: Handle image management untuk items

**Key Methods**:

- `add_image_to_item(item_id, url, order)`: Add image ke item
- `get_images_by_item(item_id)`: Get all images for item
- `update_image_order(image_id, new_order)`: Update image order
- `reorder_images(item_id, image_order_list)`: Reorder semua images
- `delete_image(image_id, user_id)`: Delete image
- `set_primary_image(image_id, user_id)`: Set primary image
- `validate_image_url(url)`: Validate URL format
- `bulk_add_images(item_id, image_urls)`: Add multiple images

## Usage dalam Routes

### Before (dengan Business Logic di Models):

```python
# Old way - business logic di model
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User()
    user.email = data['email']
    user.set_password(data['password'])
    user.save()  # Business logic di model
    return user.to_dict()
```

### After (dengan Services):

```python
# New way - business logic di service
from app.services import UserService

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user_service = UserService()
    user = user_service.create_user(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        phone=data.get('phone')
    )
    return user.to_dict()
```

## Benefits

### 1. Separation of Concerns

- **Models**: Hanya data structure dan relationships
- **Services**: Business logic dan operations
- **Routes**: HTTP handling dan validation

### 2. Reusability

Services bisa digunakan di multiple routes atau bahkan dari CLI scripts, background tasks, etc.

### 3. Testability

Business logic di services lebih mudah untuk unit testing karena terpisah dari database models.

### 4. Maintainability

Perubahan business logic hanya perlu dilakukan di satu tempat (service) bukan tersebar di models.

### 5. Single Responsibility

Setiap service memiliki tanggung jawab yang jelas dan focused.

## Service Dependencies

Services bisa menggunakan services lain:

```python
# ReviewService menggunakan ItemService dan UserService
from app.services.item_service import ItemService
from app.services.user_service import UserService

class ReviewService(BaseService):
    def create_review(self, item_id, user_id, rating, comment):
        item_service = ItemService()
        user_service = UserService()

        item = item_service.get_by_id(item_id)
        user = user_service.get_by_id(user_id)
        # ... business logic
```

## Error Handling

Services throw specific exceptions yang bisa di-catch di route handlers:

```python
try:
    booking_service = BookingService()
    booking = booking_service.create_booking(item_id, user_id, start_date, end_date)
    return booking.to_dict()
except ValueError as e:
    return {'error': str(e)}, 400
```

Dengan struktur ini, kode menjadi lebih clean, maintainable, dan mengikuti best practices software architecture.
