from sqlalchemy import select
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.review import Review
from app.models.product import Product
from app.schemas.review import LikeDislike
from app.database.redis_session import redis_connection
from app.schemas.review import ReviewCreate, ReviewResponse


class ReviewService:
  @staticmethod
  async def get_my_reviews(db: AsyncSession, user):
    reviews= await db.execute(select(Review).where(Review.user_id == user.id))
    result= reviews.scalars().all()

    return result

  @staticmethod
  async def get_review_by_id(product_id: int, db: AsyncSession):
    review= await db.execute(select(Review).where(Review.product_id==product_id))
    result= review.scalars().first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    return result

  @staticmethod
  async def create_review(review: ReviewCreate, db: AsyncSession,current_user):
    if not current_user:
      return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")

    existing_product_query = await db.execute(select(Product).where(Product.id == review.product_id))
    existing_product = existing_product_query.scalar_one_or_none()

    if not existing_product:
      raise HTTPException(detail="Product not found with that id",status_code=status.HTTP_404_NOT_FOUND)

    review_dict = review.model_dump()
    review_dict["user_id"] = current_user.id
    review_db = Review(**review_dict)
    db.add(review_db)
    await db.commit()
    await db.refresh(review_db)

    return ReviewResponse.model_validate(review_dict)

  @staticmethod
  async def update_review(
          review_id: int,
          updated_review: ReviewCreate,
          db: AsyncSession, user):

    review = await db.execute(select(Review).where(Review.id==review_id))
    review_dict = review.scalars().first()

    if not review_dict:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if review_dict.user_id != user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission to perform this action")

    review_dict.content= updated_review.content
    review_dict.rating= updated_review.rating

    db.add(review_dict)
    await db.commit()
    await db.refresh(review_dict)

    return review_dict

  @staticmethod
  async def delete_review(review_id: int, db: AsyncSession, user):
    review = await db.execute(select(Review).where(Review.id==review_id))
    review_dict= review.scalars().first()

    if not review_dict:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")

    if review_dict.user_id != user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You have no permission to perform this action")

    await db.delete(review_dict)
    await db.commit()
  
  @staticmethod
  async def like_dislike(reaction: LikeDislike, db: AsyncSession, current_user):
    review_query = await db.execute(select(Review).where(Review.id == reaction.review_id))
    review = review_query.scalars().first()

    if not review:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Review not found")

    key = f"review:{review.id}:user:{current_user.id}:reaction"
    previous_state = await redis_connection.get(key)

    like = "like"
    dislike = "dislike"

    if previous_state == like and reaction.like_dislike == 1:
        review.likes_count -= 1
        await redis_connection.delete(key)

    elif previous_state == dislike and reaction.like_dislike == 0:
        review.dislikes_count -= 1
        await redis_connection.delete(key)

    elif reaction.like_dislike == 1:
        review.likes_count += 1
        review.dislikes_count -= 1 if previous_state == dislike else 0
        await redis_connection.set(key, like)

    else:
        review.dislikes_count += 1
        review.likes_count -= 1 if previous_state == like else 0
        await redis_connection.set(key, dislike)
    
    db.add(review)
    await db.commit()
    await db.refresh(review)

    return review