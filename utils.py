import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional, List, Union
import os
from config import email_config


def send_email(
    subject: str,
    body: str,
    from_email: Optional[str] = None,
    to_email: Optional[str] = None,
    cc_emails: Optional[List[str]] = None,
    bcc_emails: Optional[List[str]] = None,
    attachments: Optional[List[str]] = None,
    is_html: bool = False
) -> bool:
    """
    Send an email using credentials from config.py
    
    Args:
        subject (str): Email subject
        body (str): Email body content
        from_email (Optional[str]): Sender email (uses default from config if not provided)
        to_email (Optional[str]): Recipient email (uses default from config if not provided)
        cc_emails (Optional[List[str]]): List of CC recipients
        bcc_emails (Optional[List[str]]): List of BCC recipients
        attachments (Optional[List[str]]): List of file paths to attach
        is_html (bool): Whether the body is HTML content (default: False)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    try:
        # Get default emails if not provided
        if not from_email:
            from_email = email_config.DEFAULT_FROM_EMAIL
        if not to_email:
            to_email = email_config.DEFAULT_TO_EMAIL
            
        # Get email credentials and SMTP config
        username, password = email_config.get_email_credentials()
        smtp_config = email_config.get_smtp_config()
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = from_email
        message["To"] = to_email
        
        # Add CC recipients if provided
        if cc_emails:
            message["Cc"] = ", ".join(cc_emails)
            
        # Prepare all recipients
        all_recipients = [to_email]
        if cc_emails:
            all_recipients.extend(cc_emails)
        if bcc_emails:
            all_recipients.extend(bcc_emails)
        
        # Add body to email
        if is_html:
            html_part = MIMEText(body, "html")
            message.attach(html_part)
        else:
            text_part = MIMEText(body, "plain")
            message.attach(text_part)
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    filename = os.path.basename(file_path)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    message.attach(part)
        
        # Create SMTP session
        if smtp_config["use_ssl"]:
            # Use SSL
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(smtp_config["server"], smtp_config["port"], context=context)
        else:
            # Use TLS or no encryption
            server = smtplib.SMTP(smtp_config["server"], smtp_config["port"])
            if smtp_config["use_tls"]:
                context = ssl.create_default_context()
                server.starttls(context=context)
        
        # Login and send email
        server.login(username, password)
        server.sendmail(from_email, all_recipients, message.as_string())
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False


def send_simple_email(subject: str, message: str) -> bool:
    """
    Send a simple email using default configuration
    
    Args:
        subject (str): Email subject
        message (str): Email message
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    return send_email(subject=subject, body=message)


def send_html_email(subject: str, html_content: str) -> bool:
    """
    Send an HTML email using default configuration
    
    Args:
        subject (str): Email subject
        html_content (str): HTML email content
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    return send_email(subject=subject, body=html_content, is_html=True)


def test_email_configuration() -> bool:
    """
    Test email configuration by sending a test email
    
    Returns:
        bool: True if test email sent successfully, False otherwise
    """
    test_subject = "Email Configuration Test"
    test_body = """
    This is a test email to verify that the email configuration is working correctly.
    
    If you receive this email, the configuration is valid.
    
    Best regards,
    Webhook System
    """
    
    return send_simple_email(test_subject, test_body)