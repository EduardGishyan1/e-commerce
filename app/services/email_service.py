import uuid
import requests

from sqlalchemy import select
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.config.settings import settings
from app.database.redis_session import redis_connection
from app.responses.notification_messages import EmailConstants


def generate_verification_token():
  return str(uuid.uuid4().hex[:6].upper())

async def store_verification_token(user_email: str, token: str, expiry: int = 3600):
  await redis_connection.set(token, user_email, ex=expiry)

class EmailService:
  @staticmethod
  async def __send_email(to_email: str, subject: str, body: str):
    if not settings.SENDGRID_API_KEY or not settings.FROM_EMAIL:
      return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Missing SENDGRID_API_KEY or FROM_EMAIL in environment variables.")

    try:
      message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=body)
      sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
      response = await sg.send(message)

      if response.status_code != 202:
        return HTTPException(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          detail=f"Failed to send email. Status code: {response.status_code}. Response: {response.body}")

      return response

    except requests.exceptions.RequestException as e:
      return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=f"Network error while sending email: {str(e)}")

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"An unexpected error occurred: {str(e)}")

  @staticmethod
  async def send_verification_email(to_email: str):
    token = generate_verification_token()
    await store_verification_token(to_email, token)
    verification_link = f"https://localhost:3003/auth/verify-email"
    subject = EmailConstants.email_verify_subject()
    body = EmailConstants.email_verify_body(token, verification_link)
    return await EmailService.__send_email(to_email, subject, body)

  @staticmethod
  async def update_message(to_email: str):
    try:
      subject = EmailConstants.update_subject()
      body = EmailConstants.update_body()
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return e

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending update email: {str(e)}")

  @staticmethod
  async def change_password_message(to_email:str):
    try:
      subject = EmailConstants.change_password()
      body = EmailConstants.change_password_body()
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return {"message": str(e)}

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending update email: {str(e)}")

  @staticmethod
  async def deletion_message(to_email: str):
    try:
      subject = EmailConstants.deletion_subject()
      body = EmailConstants.deletion_body()
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return e

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending deletion email: {str(e)}")

  @staticmethod
  async def order_placement_message(to_email: str):
    try:
      subject = EmailConstants.order_placement_subject()
      body = EmailConstants.order_placement_body()
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return e

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending order placement email: {str(e)}")

  @staticmethod
  async def payment_confirmation_message(to_email: str):
    try:
      subject = EmailConstants.payment_confirmation_subject()
      body = EmailConstants.payment_confirmation_body()
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return e

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending payment confirmation email: {str(e)}")

  @staticmethod
  async def password_recovery_email(to_email: str):
    try:
      subject = EmailConstants.password_reset_subject()
      token = generate_verification_token()
      await store_verification_token(to_email, token)
      password_recovery_link=f"https://localhost:3003/auth/password_recovery"
      body = EmailConstants.password_reset_body(token, password_recovery_link)
      return await EmailService.__send_email(to_email, subject, body)

    except HTTPException as e:
      return e

    except Exception as e:
      return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Error while sending password reset email: {str(e)}")

  @staticmethod
  async def verify_email(token,db: AsyncSession):
    user_email = await redis_connection.get(token)
    if not user_email:
      raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = await db.execute(select(User).where(User.email == user_email))
    if not user:
      raise HTTPException(status_code=404, detail="User not found")

    user_db= user.scalars().first()
    user_db.is_verified = True

    await db.commit()
    await db.refresh(user_db)

    await redis_connection.delete(f"email_verification:{user_email}")

    return {"message": "Email verified successfully"}