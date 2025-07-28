#!/usr/bin/env python3
"""
Test script to verify email provider detection logic.
"""

# Test the email provider detection logic
def _is_common_email_provider(email):
    """
    Check if the email domain is from a common email service provider.
    
    Args:
        email (str): Email address to check
        
    Returns:
        bool: True if email is from a common provider, False otherwise
    """
    if not email or '@' not in email:
        return False
        
    domain = email.lower().split('@')[1]
    
    # List of common email service providers
    common_providers = {
        'gmail.com', 'googlemail.com',
        'outlook.com', 'hotmail.com', 'live.com', 'msn.com',
        'yahoo.com', 'yahoo.co.uk', 'yahoo.ca', 'yahoo.co.in', 'yahoo.com.au',
        'icloud.com', 'me.com', 'mac.com',
        'protonmail.com', 'proton.me',
        'aol.com',
        'mail.com',
        'yandex.com', 'yandex.ru',
        'zoho.com',
        'tutanota.com',
        'fastmail.com'
    }
    
    return domain in common_providers

def _get_recipient_email(user_email):
    """
    Get the actual recipient email address for testing purposes.
    If user email is not from a common provider, use test bowl instead.
    
    Args:
        user_email (str): Original user email address
        
    Returns:
        str: Email address to send to (either original or test bowl)
    """
    test_bowl = "t0pramen19@gmail.com"
    
    if _is_common_email_provider(user_email):
        return user_email
    else:
        print(f"Non-common email provider detected ({user_email}), using test bowl: {test_bowl}")
        return test_bowl

# Test cases
test_emails = [
    "john.doe@gmail.com",  # Should use original (common)
    "test@outlook.com",    # Should use original (common)  
    "user@yahoo.com",      # Should use original (common)
    "john@doe.com",        # Should use test bowl (non-common)
    "user@company.co.id",  # Should use test bowl (non-common)
    "admin@example.org",   # Should use test bowl (non-common)
    "t0pramen19@gmail.com" # Should use original (common)
]

print("Testing email provider detection logic:")
print("=" * 50)

for email in test_emails:
    is_common = _is_common_email_provider(email)
    recipient = _get_recipient_email(email)
    
    print(f"Email: {email}")
    print(f"  Common provider: {is_common}")
    print(f"  Recipient: {recipient}")
    print(f"  Redirected: {'Yes' if recipient != email else 'No'}")
    print()
