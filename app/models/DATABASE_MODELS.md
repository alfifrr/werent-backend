# Database Models dan Relationships - WeRent Backend

## Overview

Database models untuk platform peer-to-peer rental telah dibuat sesuai dengan schema diagram. Semua model menggunakan `back_populates` untuk mendefinisikan relasi yang jelas dan bidirectional.

## Models yang Dibuat

### 1. User Model (`app/models/user.py`)

**Table**: `users`

**Fields**:

- `id` (Primary Key)
- `email` (Unique, Index)
- `password_hash`
- `name`
- `phone`
- `created_at`
- `is_verified`
- `avg_rating` (untuk rating sebagai pemilik item)

**Relationships**:

- `owned_items`: One-to-Many dengan Item (sebagai owner)
- `rented_items`: One-to-Many dengan Booking (sebagai renter)
- `sent_messages`: One-to-Many dengan Message (sebagai sender)
- `received_messages`: One-to-Many dengan Message (sebagai receiver)
- `written_reviews`: One-to-Many dengan Review (sebagai reviewer)

### 2. Item Model (`app/models/item.py`)

**Table**: `items`

**Fields**:

- `id` (Primary Key)
- `title`
- `description`
- `price_per_day`
- `status` (available, rented, maintenance)
- `category`
- `created_at`
- `owner_id` (Foreign Key ke users)

**Relationships**:

- `owner`: Many-to-One dengan User
- `images`: One-to-Many dengan Image
- `bookings`: One-to-Many dengan Booking
- `reviews`: One-to-Many dengan Review

### 3. Image Model (`app/models/image.py`)

**Table**: `images`

**Fields**:

- `id` (Primary Key)
- `url`
- `order` (untuk urutan tampilan gambar)
- `item_id` (Foreign Key ke items)

**Relationships**:

- `item`: Many-to-One dengan Item

### 4. Booking Model (`app/models/booking.py`)

**Table**: `bookings`

**Fields**:

- `id` (Primary Key)
- `start_date`
- `end_date`
- `status` (pending, confirmed, completed, cancelled)
- `total_price`
- `created_at`
- `item_id` (Foreign Key ke items)
- `renter_id` (Foreign Key ke users)

**Relationships**:

- `item`: Many-to-One dengan Item
- `renter`: Many-to-One dengan User

### 5. Message Model (`app/models/message.py`)

**Table**: `messages`

**Fields**:

- `id` (Primary Key)
- `content`
- `sent_at`
- `is_read`
- `sender_id` (Foreign Key ke users)
- `receiver_id` (Foreign Key ke users)

**Relationships**:

- `sender`: Many-to-One dengan User
- `receiver`: Many-to-One dengan User

### 6. Review Model (`app/models/review.py`)

**Table**: `reviews`

**Fields**:

- `id` (Primary Key)
- `rating` (1-5)
- `comment`
- `created_at`
- `item_id` (Foreign Key ke items)
- `user_id` (Foreign Key ke users)

**Relationships**:

- `item`: Many-to-One dengan Item
- `user`: Many-to-One dengan User

### 7. Category Model (`app/models/category.py`)

**Table**: `categories` (Optional - untuk better organization)

**Fields**:

- `id` (Primary Key)
- `name` (Unique)
- `description`
- `is_active`

## Relationship Mapping

### User Relationships:

```python
# Sebagai pemilik item
user.owned_items -> List[Item]

# Sebagai penyewa
user.rented_items -> List[Booking]

# Pesan yang dikirim
user.sent_messages -> List[Message]

# Pesan yang diterima
user.received_messages -> List[Message]

# Review yang ditulis
user.written_reviews -> List[Review]
```

### Item Relationships:

```python
# Pemilik item
item.owner -> User

# Gambar-gambar item
item.images -> List[Image]

# Booking untuk item ini
item.bookings -> List[Booking]

# Review untuk item ini
item.reviews -> List[Review]
```

### Booking Relationships:

```python
# Item yang dibooking
booking.item -> Item

# User yang melakukan booking
booking.renter -> User
```

### Message Relationships:

```python
# Pengirim pesan
message.sender -> User

# Penerima pesan
message.receiver -> User
```

### Review Relationships:

```python
# Item yang direview
review.item -> Item

# User yang menulis review
review.user -> User
```

## Key Features

### 1. Automatic Relationship Handling

Semua relationships menggunakan `back_populates` untuk akses bidirectional yang aman.

### 2. Cascade Operations

- Ketika Item dihapus, semua Image akan ikut terhapus (cascade='all, delete-orphan')

### 3. Business Logic Methods

Setiap model dilengkapi dengan methods untuk:

- CRUD operations
- Status management
- Calculations (rating, pricing, duration)
- Validation

### 4. Automatic Rating Updates

Review model secara otomatis mengupdate `avg_rating` user ketika review baru ditambahkan atau diupdate.

### 5. Smart Querying

Methods untuk query data dengan berbagai filter dan kondisi bisnis.

## Usage Examples

```python
# Membuat user baru
user = User()
user.email = "user@example.com"
user.name = "John Doe"
user.set_password("password123")
user.save()

# Membuat item
item = Item()
item.title = "Canon EOS R5"
item.description = "Professional camera"
item.price_per_day = 100.0
item.owner_id = user.id
item.save()

# Menambahkan gambar
image = Image()
image.url = "https://example.com/camera.jpg"
image.item_id = item.id
image.save()

# Membuat booking
booking = Booking()
booking.item_id = item.id
booking.renter_id = another_user.id
booking.start_date = datetime(2025, 8, 1)
booking.end_date = datetime(2025, 8, 5)
booking.total_price = booking.calculate_total_price()
booking.save()

# Akses relationships
print(f"Item owner: {item.owner.name}")
print(f"Item images: {[img.url for img in item.images]}")
print(f"User's items: {[item.title for item in user.owned_items]}")
```

## Database Migration

Setelah models dibuat, jalankan migration untuk membuat tables:

```bash
# Jika menggunakan Flask-Migrate
flask db init
flask db migrate -m "Create all tables"
flask db upgrade
```

Models ini sudah siap untuk digunakan dan mengikuti best practices SQLAlchemy dengan relationships yang jelas dan business logic yang lengkap.
