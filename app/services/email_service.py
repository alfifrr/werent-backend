"""
Email service for WeRent Backend API.
Handles sending verification emails and other email communications.
"""

from flask import current_app, url_for
from flask_mail import Message
from app.extensions import mail


class EmailService:
    """Service class for handling email operations."""

    @staticmethod
    def send_verification_email(user_email, user_name, verification_uuid):
        """
        Send email verification email to user.
        
        Args:
            user_email (str): User's email address
            user_name (str): User's full name
            verification_uuid (str): UUID for email verification
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            # Create verification URL
            verification_url = url_for(
                'auth.verify_email', 
                uuid=verification_uuid, 
                _external=True
            )
            
            # Create email message
            subject = "Welcome to WeRent - Please Verify Your Email"
            
            # HTML email template
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Email Verification - WeRent</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        text-align: center;
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        border-radius: 10px 10px 0 0;
                    }}
                    .content {{
                        background-color: #f9f9f9;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }}
                    .button {{
                        display: inline-block;
                        background-color: #4CAF50;
                        color: white;
                        padding: 12px 30px;
                        text-decoration: none;
                        border-radius: 5px;
                        margin: 20px 0;
                        font-weight: bold;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Welcome to WeRent!</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name}!</h2>
                    <p>Thank you for signing up with WeRent, your trusted equipment rental platform.</p>
                    <p>To complete your registration and start renting amazing equipment, please verify your email address by clicking the button below:</p>
                    
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify My Email Address</a>
                    </div>
                    
                    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                    <p><a href="{verification_url}">{verification_url}</a></p>
                    
                    <p><strong>Important:</strong> This verification link will expire in 24 hours for security reasons.</p>
                    
                    <p>If you didn't create an account with WeRent, please ignore this email.</p>
                    
                    <p>Best regards,<br>The WeRent Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 WeRent. All rights reserved.</p>
                    <p>This is an automated email, please do not reply.</p>
                </div>
            </body>
            </html>
            """
            
            # Plain text version for email clients that don't support HTML
            text_body = f"""
            Welcome to WeRent!
            
            Hello {user_name}!
            
            Thank you for signing up with WeRent, your trusted equipment rental platform.
            
            To complete your registration and start renting amazing equipment, please verify your email address by visiting this link:
            
            {verification_url}
            
            Important: This verification link will expire in 24 hours for security reasons.
            
            If you didn't create an account with WeRent, please ignore this email.
            
            Best regards,
            The WeRent Team
            
            © 2025 WeRent. All rights reserved.
            This is an automated email, please do not reply.
            """
            
            # Create and send message
            msg = Message(
                subject=subject,
                recipients=[user_email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            current_app.logger.info(f"Verification email sent successfully to {user_email}")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send verification email to {user_email}: {str(e)}")
            return False

    @staticmethod
    def send_welcome_email(user_email, user_name):
        """
        Send welcome email after successful email verification.
        
        Args:
            user_email (str): User's email address
            user_name (str): User's full name
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            subject = "Welcome to WeRent - Your Account is Ready!"
            
            html_body = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Welcome to WeRent</title>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        max-width: 600px;
                        margin: 0 auto;
                        padding: 20px;
                    }}
                    .header {{
                        text-align: center;
                        background-color: #4CAF50;
                        color: white;
                        padding: 20px;
                        border-radius: 10px 10px 0 0;
                    }}
                    .content {{
                        background-color: #f9f9f9;
                        padding: 30px;
                        border-radius: 0 0 10px 10px;
                    }}
                    .feature {{
                        background-color: white;
                        padding: 15px;
                        margin: 10px 0;
                        border-radius: 5px;
                        border-left: 4px solid #4CAF50;
                    }}
                    .footer {{
                        text-align: center;
                        margin-top: 20px;
                        color: #666;
                        font-size: 12px;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>🎉 Welcome to WeRent!</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name}!</h2>
                    <p>Congratulations! Your email has been verified and your WeRent account is now active.</p>
                    
                    <h3>What you can do now:</h3>
                    <div class="feature">
                        <strong>📸 Browse Equipment</strong><br>
                        Discover thousands of rental items from cameras to outdoor gear.
                    </div>
                    
                    <div class="feature">
                        <strong>📅 Make Bookings</strong><br>
                        Reserve equipment for your next adventure or project.
                    </div>
                    
                    <div class="feature">
                        <strong>💰 List Your Items</strong><br>
                        Earn money by renting out your own equipment.
                    </div>
                    
                    <div class="feature">
                        <strong>⭐ Leave Reviews</strong><br>
                        Help the community by reviewing your rental experiences.
                    </div>
                    
                    <p>Ready to get started? Log in to your account and explore what WeRent has to offer!</p>
                    
                    <p>If you have any questions, feel free to contact our support team.</p>
                    
                    <p>Happy renting!<br>The WeRent Team</p>
                </div>
                <div class="footer">
                    <p>© 2025 WeRent. All rights reserved.</p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Welcome to WeRent!
            
            Hello {user_name}!
            
            Congratulations! Your email has been verified and your WeRent account is now active.
            
            What you can do now:
            • Browse Equipment - Discover thousands of rental items
            • Make Bookings - Reserve equipment for your adventures
            • List Your Items - Earn money by renting out your equipment
            • Leave Reviews - Help the community with your feedback
            
            Ready to get started? Log in to your account and explore what WeRent has to offer!
            
            Happy renting!
            The WeRent Team
            
            © 2025 WeRent. All rights reserved.
            """
            
            msg = Message(
                subject=subject,
                recipients=[user_email],
                html=html_body,
                body=text_body
            )
            
            mail.send(msg)
            current_app.logger.info(f"Welcome email sent successfully to {user_email}")
            return True
            
        except Exception as e:
            current_app.logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
            return False
