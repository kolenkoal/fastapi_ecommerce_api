import smtplib

from pydantic import EmailStr

from src.config import settings
from src.tasks.celery_settings import celery
from src.tasks.email_templates import create_reset_password_template


@celery.task
def send_password_reset_email(
    email_to: EmailStr, user_first_name, token  # noqa
):
    # email_to = settings.SMTP_USER
    msg_content = create_reset_password_template(
        email_to, user_first_name, token
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(
            settings.EMAIL_SENDER_USERNAME, settings.EMAIL_SENDER_PASSWORD
        )
        server.send_message(msg_content)
