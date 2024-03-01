from email.message import EmailMessage

from pydantic import EmailStr

from src.config import settings


def create_reset_password_template(email_to: EmailStr, user_first_name, token):
    email = EmailMessage()

    email["From"] = settings.EMAIL_SENDER_USERNAME
    email["To"] = email_to
    email["Subject"] = "Password reset"

    email.set_content(
        f"""
            <h1>Reset password</h1>
            Hi, dear {user_first_name}.\n\nYou have asked for
            password rest. Here is your token for resetting your
            password: \n{token}. Navigate to /api/auth/reset-password,
             insert this token and desired password.
        """,
        subtype="html",
    )
    return email
