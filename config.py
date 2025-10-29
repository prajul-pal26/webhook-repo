import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailConfig:
    """Email configuration settings"""
    
    # SMTP Server Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    
    # Email Credentials
    EMAIL_USERNAME: str = os.getenv("EMAIL_USERNAME", "nikadeep26@gmail.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "oirvllccrrrpecpp")
    
    # Default Email Addresses
    DEFAULT_FROM_EMAIL: str = os.getenv("DEFAULT_FROM_EMAIL", "nikadeep26@gmail.com")
    DEFAULT_TO_EMAIL: str = os.getenv("DEFAULT_TO_EMAIL", "pranjulpal04@gmail.com")
    
    # Email Settings
    USE_TLS: bool = os.getenv("USE_TLS", "true").lower() == "true"
    USE_SSL: bool = os.getenv("USE_SSL", "false").lower() == "true"
    
    @classmethod
    def get_email_credentials(cls) -> tuple:
        """Get email credentials as a tuple"""
        return (cls.EMAIL_USERNAME, cls.EMAIL_PASSWORD)
    
    @classmethod
    def get_smtp_config(cls) -> dict:
        """Get SMTP configuration as a dictionary"""
        return {
            "server": cls.SMTP_SERVER,
            "port": cls.SMTP_PORT,
            "use_tls": cls.USE_TLS,
            "use_ssl": cls.USE_SSL
        }
    
    @classmethod
    def get_default_emails(cls) -> tuple:
        """Get default from and to emails as a tuple"""
        return (cls.DEFAULT_FROM_EMAIL, cls.DEFAULT_TO_EMAIL)

# Create a global instance
email_config = EmailConfig()