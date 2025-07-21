"""
Schemas package for WeRent Backend API.
Contains all Pydantic schemas for request/response validation using @field_validator.
"""

# Base schemas
from .base_schema import (
    BaseSchema,
    TimestampMixin,
    ResponseSchema,
    PaginationSchema,
    PaginatedResponseSchema
)

# User schemas
from .user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserUpdateSchema,
    UserPasswordUpdateSchema,
    UserResponseSchema,
    UserProfileResponseSchema,
    UserListResponseSchema,
    UserStatsSchema,
    UserSearchSchema,
    UserVerificationSchema
)

# Authentication schemas
from .auth_schema import (
    LoginSchema,
    LoginResponseSchema,
    RegisterSchema,
    RegisterResponseSchema,
    TokenRefreshSchema,
    TokenResponseSchema,
    PasswordResetRequestSchema,
    PasswordResetSchema,
    EmailVerificationSchema,
    EmailVerificationRequestSchema,
    ChangePasswordSchema,
    LogoutSchema,
    AuthStatusSchema,
    TwoFactorAuthSchema,
    TwoFactorSetupSchema
)

# Item schemas
from .item_schema import (
    ItemCreateSchema,
    ItemUpdateSchema,
    ItemStatusUpdateSchema,
    ItemResponseSchema,
    ItemDetailResponseSchema,
    ItemListResponseSchema,
    ItemSearchSchema,
    ItemFilterSchema,
    ItemStatsSchema,
    ItemAvailabilitySchema,
    ItemAvailabilityResponseSchema,
    CategoryStatsSchema
)

# Booking schemas
from .booking_schema import (
    BookingCreateSchema,
    BookingUpdateSchema,
    BookingStatusUpdateSchema,
    BookingExtendSchema,
    BookingResponseSchema,
    BookingDetailResponseSchema,
    BookingListResponseSchema,
    BookingSearchSchema,
    BookingStatsSchema,
    BookingCalendarSchema,
    BookingCalendarResponseSchema,
    BookingAvailabilityCheckSchema,
    BookingAvailabilityResponseSchema,
    BookingRevenueSchema,
    BookingRevenueResponseSchema
)

# Message schemas
from .message_schema import (
    MessageCreateSchema,
    MessageUpdateSchema,
    MessageResponseSchema,
    MessageDetailResponseSchema,
    MessageListResponseSchema,
    ConversationSchema,
    ConversationResponseSchema,
    ConversationListResponseSchema,
    MessageSearchSchema,
    MessageStatsSchema,
    UnreadMessageCountSchema,
    MessageMarkReadSchema
)

# Review schemas
from .review_schema import (
    ReviewCreateSchema,
    ReviewUpdateSchema,
    ReviewResponseSchema,
    ReviewDetailResponseSchema,
    ReviewListResponseSchema,
    ReviewSearchSchema,
    ReviewStatsSchema,
    ReviewRatingDistributionSchema
)

# Image schemas
from .image_schema import (
    ImageCreateSchema,
    ImageUpdateSchema,
    ImageResponseSchema,
    ImageListResponseSchema,
    ItemImagesResponseSchema,
    ImageUploadSchema,
    ImageUploadResponseSchema
)

# Error schemas
from .error_schema import (
    ErrorSchema,
    ValidationErrorSchema,
    NotFoundErrorSchema,
    UnauthorizedErrorSchema,
    ForbiddenErrorSchema,
    ConflictErrorSchema,
    BusinessLogicErrorSchema,
    BookingErrorSchema,
    ItemUnavailableErrorSchema,
    RateLimitErrorSchema,
    InternalServerErrorSchema
)

__all__ = [
    # Base
    'BaseSchema',
    'TimestampMixin',
    'ResponseSchema',
    'PaginationSchema',
    'PaginatedResponseSchema',

    # User
    'UserCreateSchema',
    'UserLoginSchema',
    'UserUpdateSchema',
    'UserPasswordUpdateSchema',
    'UserResponseSchema',
    'UserProfileResponseSchema',
    'UserListResponseSchema',
    'UserStatsSchema',
    'UserSearchSchema',
    'UserVerificationSchema',

    # Auth
    'LoginSchema',
    'LoginResponseSchema',
    'RegisterSchema',
    'RegisterResponseSchema',
    'TokenRefreshSchema',
    'TokenResponseSchema',
    'PasswordResetRequestSchema',
    'PasswordResetSchema',
    'EmailVerificationSchema',
    'EmailVerificationRequestSchema',
    'ChangePasswordSchema',
    'LogoutSchema',
    'AuthStatusSchema',
    'TwoFactorAuthSchema',
    'TwoFactorSetupSchema',

    # Item
    'ItemCreateSchema',
    'ItemUpdateSchema',
    'ItemStatusUpdateSchema',
    'ItemResponseSchema',
    'ItemDetailResponseSchema',
    'ItemListResponseSchema',
    'ItemSearchSchema',
    'ItemFilterSchema',
    'ItemStatsSchema',
    'ItemAvailabilitySchema',
    'ItemAvailabilityResponseSchema',
    'CategoryStatsSchema',

    # Booking
    'BookingCreateSchema',
    'BookingUpdateSchema',
    'BookingStatusUpdateSchema',
    'BookingExtendSchema',
    'BookingResponseSchema',
    'BookingDetailResponseSchema',
    'BookingListResponseSchema',
    'BookingSearchSchema',
    'BookingStatsSchema',
    'BookingCalendarSchema',
    'BookingCalendarResponseSchema',
    'BookingAvailabilityCheckSchema',
    'BookingAvailabilityResponseSchema',
    'BookingRevenueSchema',
    'BookingRevenueResponseSchema',

    # Message
    'MessageCreateSchema',
    'MessageUpdateSchema',
    'MessageResponseSchema',
    'MessageDetailResponseSchema',
    'MessageListResponseSchema',
    'ConversationSchema',
    'ConversationResponseSchema',
    'ConversationListResponseSchema',
    'MessageSearchSchema',
    'MessageStatsSchema',
    'UnreadMessageCountSchema',
    'MessageMarkReadSchema',

    # Review
    'ReviewCreateSchema',
    'ReviewUpdateSchema',
    'ReviewResponseSchema',
    'ReviewDetailResponseSchema',
    'ReviewListResponseSchema',
    'ReviewSearchSchema',
    'ReviewStatsSchema',
    'ReviewRatingDistributionSchema',

    # Image
    'ImageCreateSchema',
    'ImageUpdateSchema',
    'ImageResponseSchema',
    'ImageListResponseSchema',
    'ItemImagesResponseSchema',
    'ImageUploadSchema',
    'ImageUploadResponseSchema',

    # Error
    'ErrorSchema',
    'ValidationErrorSchema',
    'NotFoundErrorSchema',
    'UnauthorizedErrorSchema',
    'ForbiddenErrorSchema',
    'ConflictErrorSchema',
    'BusinessLogicErrorSchema',
    'BookingErrorSchema',
    'ItemUnavailableErrorSchema',
    'RateLimitErrorSchema',
    'InternalServerErrorSchema',
]