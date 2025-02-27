from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_contact_email(contact):
        """
        Send email notification for contact form submissions
        """
        try:
            # Prepare email content
            context = {
                'name': contact.name,
                'email': contact.email,
                'subject': contact.subject,
                'message': contact.message,
                'created_at': contact.created_at
            }
            
            html_message = render_to_string('emails/contact_notification.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=f'New Contact Form Submission: {contact.subject}',
                message=plain_message,
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            logger.info(f"Contact form email sent successfully for {contact.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send contact form email: {str(e)}")
            return False

    @staticmethod
    def send_inquiry_email(inquiry):
        """
        Send email notification for product inquiries
        """
        try:
            # Get product details
            product_details = []
            for item in inquiry.items.all():
                product_details.append({
                    'name': item.product.name,
                    'style_number': item.product.style_number,
                    'price': item.product.price
                })

            # Prepare email content
            context = {
                'name': inquiry.name,
                'email': inquiry.email,
                'subject': inquiry.subject,
                'message': inquiry.message,
                'created_at': inquiry.created_at,
                'products': product_details
            }
            
            html_message = render_to_string('emails/inquiry_notification.html', context)
            plain_message = strip_tags(html_message)
            
            send_mail(
                subject=f'New Product Inquiry: {inquiry.subject}',
                message=plain_message,
                html_message=html_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            logger.info(f"Inquiry email sent successfully for {inquiry.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send inquiry email: {str(e)}")
            return False 