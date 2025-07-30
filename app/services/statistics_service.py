from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import User, Item, Booking, Payment, Review, Ticketing
from datetime import UTC
from calendar import monthrange



def get_admin_statistics():
    db = User.query.session
    """
    Returns admin dashboard statistics: totals and weekly stats for users, items, bookings, revenue, reviews, and tickets.
    """
    # Total counts
    total_users = db.query(func.count(User.id)).scalar()
    total_items = db.query(func.count(Item.id)).scalar()
    total_bookings = db.query(func.count(Booking.id)).scalar()
    total_revenue = db.query(func.coalesce(func.sum(Payment.total_price), 0)).scalar()
    total_reviews = db.query(func.count(Review.id)).scalar()
    total_tickets = db.query(func.count(Ticketing.id)).scalar()

    # Weekly statistics (last 7 days)
    week_ago = datetime.now(UTC) - timedelta(days=7)
    weekly_users = (
        db.query(func.count(User.id)).filter(User.created_at >= week_ago).scalar()
        if hasattr(User, "created_at")
        else None
    )
    weekly_items = (
        db.query(func.count(Item.id)).filter(Item.created_at >= week_ago).scalar()
        if hasattr(Item, "created_at")
        else None
    )
    weekly_bookings = (
        db.query(func.count(Booking.id)).filter(Booking.created_at >= week_ago).scalar()
        if hasattr(Booking, "created_at")
        else None
    )
    weekly_revenue = (
        db.query(func.coalesce(func.sum(Payment.total_price), 0))
        .filter(Payment.payment_date >= week_ago)
        .scalar()
        if hasattr(Payment, "payment_date")
        else None
    )
    weekly_reviews = (
        db.query(func.count(Review.id)).filter(Review.created_at >= week_ago).scalar()
        if hasattr(Review, "created_at")
        else None
    )
    weekly_tickets = (
        db.query(func.count(Ticketing.id))
        .filter(Ticketing.created_at >= week_ago)
        .scalar()
        if hasattr(Ticketing, "created_at")
        else None
    )

    return {
        "total_users": total_users,
        "total_items": total_items,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "total_reviews": total_reviews,
        "total_tickets": total_tickets,
        "weekly": {
            "users": weekly_users,
            "items": weekly_items,
            "bookings": weekly_bookings,
            "revenue": weekly_revenue,
            "reviews": weekly_reviews,
            "tickets": weekly_tickets,
        },
    }


def get_monthly_statistics(year):
    db = User.query.session
    """
    Returns monthly statistics for the provided year.
    Output: {
        'users': [count for each month],
        'items': [...],
        'bookings': [...],
        'revenue': [...],
        'reviews': [...],
        'tickets': [...],
    }
    """
    stats = {
        'users': [],
        'items': [],
        'bookings': [],
        'revenue': [],
        'reviews': [],
        'tickets': []
    }
    for month in range(1, 13):
        start = datetime(year, month, 1, tzinfo=UTC)
        last_day = monthrange(year, month)[1]
        end = datetime(year, month, last_day, 23, 59, 59, tzinfo=UTC)
        # Users
        users = db.query(func.count(User.id)).filter(
            getattr(User, 'created_at', None) is not None,
            User.created_at >= start,
            User.created_at <= end
        ).scalar() if hasattr(User, 'created_at') else None
        # Items
        items = db.query(func.count(Item.id)).filter(
            getattr(Item, 'created_at', None) is not None,
            Item.created_at >= start,
            Item.created_at <= end
        ).scalar() if hasattr(Item, 'created_at') else None
        # Bookings
        bookings = db.query(func.count(Booking.id)).filter(
            getattr(Booking, 'created_at', None) is not None,
            Booking.created_at >= start,
            Booking.created_at <= end
        ).scalar() if hasattr(Booking, 'created_at') else None
        # Revenue
        revenue = db.query(func.coalesce(func.sum(Payment.total_price), 0)).filter(
            getattr(Payment, 'payment_date', None) is not None,
            Payment.payment_date >= start,
            Payment.payment_date <= end
        ).scalar() if hasattr(Payment, 'payment_date') else None
        # Reviews
        reviews = db.query(func.count(Review.id)).filter(
            getattr(Review, 'created_at', None) is not None,
            Review.created_at >= start,
            Review.created_at <= end
        ).scalar() if hasattr(Review, 'created_at') else None
        # Tickets
        tickets = db.query(func.count(Ticketing.id)).filter(
            getattr(Ticketing, 'created_at', None) is not None,
            Ticketing.created_at >= start,
            Ticketing.created_at <= end
        ).scalar() if hasattr(Ticketing, 'created_at') else None
        stats['users'].append(users)
        stats['items'].append(items)
        stats['bookings'].append(bookings)
        stats['revenue'].append(revenue)
        stats['reviews'].append(reviews)
        stats['tickets'].append(tickets)
    return stats

