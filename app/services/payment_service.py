import stripe
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import settings
from app.models.order import Order
from app.models.payment import Payment
from app.models.user import User
from app.schemas.order import OrderStatus
from app.schemas.payment import PaymentCreate, PaymentStatus
from app.services.email_service import EmailService

publishable_key = settings.STRIPE_PUBLIC_KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentServiceStripe:
  @staticmethod
  async def create_checkout_session(
          request: PaymentCreate,
          db: AsyncSession, current_user):
    query = select(Order).where(Order.id == request.order_id).filter(Order.order_status == OrderStatus.pending)
    result = await db.execute(query)
    order = result.scalars().first()

    if not order:
      raise HTTPException(status_code=404, detail="Order not found")

    if order.user_id != current_user.id:
      raise HTTPException(status_code=403, detail="Unauthorized to make payment for this order")

    session = stripe.checkout.Session.create(
      payment_method_types=["card"],
      line_items=[{
        "price_data": {
          "currency": request.currency,
          "unit_amount": int(order.total_amount) * 100,
          "product_data": {"name": f"Order {order.id}"},
        },
        "quantity": 1,
      }],
      mode="payment",
      success_url="http://localhost:3003/payments/success?session_id={CHECKOUT_SESSION_ID}",
      cancel_url="http://localhost:3003/payments/cancel?session_id={CHECKOUT_SESSION_ID}",
    )

    new_payment = Payment(
      amount=order.total_amount,
      currency=request.currency,
      user_id=current_user.id,
      order_id=order.id,
      stripe_session_id=session.id,
      status=PaymentStatus.pending)

    db.add(new_payment)
    await db.commit()
    await db.refresh(new_payment)
    return {"session_id": session.id, "checkout_url": session.url}

  @staticmethod
  async def handle_webhook(event: dict, db: AsyncSession):
    if event["type"] == "checkout.session.completed":
      session = event["data"]["object"]
      stripe_session_id = session["id"]

      result = await db.execute(select(Payment).where(Payment.stripe_session_id == stripe_session_id))
      payment = result.scalars().first()

      if payment:
        payment.status = PaymentStatus.completed

      user_query = await db.execute(select(User).where(User.id == payment.user_id))
      user = user_query.scalars().first()

      if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

      db.add(payment)
      await db.commit()
      await db.refresh(payment)

      await EmailService.payment_confirmation_message(user.email)

    elif event["type"] == "checkout.session.expired":
      session = event["data"]["object"]
      stripe_session_id = session["id"]

      result = await db.execute(select(Payment).where(Payment.stripe_session_id == stripe_session_id))
      payment = result.scalars().first()

      if payment:
        payment.status = PaymentStatus.failed

      db.add(payment)
      await db.commit()
      await db.refresh(payment)