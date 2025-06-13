from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.services.auth_service import AuthService
from app.services.email_service import EmailService
from app.schemas.user import UserCreate, UserLogin
from app.responses.user_responses import user_responses
from app.responses.register_response import auth_email, register_responses


router = APIRouter(prefix="/auth", tags=["Auth"])

BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "static")

@router.post("/register", responses=register_responses,
             status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserCreate,
        db: AsyncSession = Depends(get_db)):
  try:
    users = await AuthService.register_user(user_data, db)
    return users
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/login", responses=user_responses)
async def login_user(
        user: UserLogin,
        response:Response,
        db: AsyncSession = Depends(get_db)):
  try:
    result = await AuthService.login_user(user.email, user.password, response, db)
    return result
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/logout")
async def logout(request: Request, response: Response):
  try:
    message = await AuthService.logout_user(request,response)
    return message
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/verify-email")
async def verify_email(request: Request):
  try:
    return templates.TemplateResponse("email-verification.html",{"request":request})
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
  
@router.post("/verify-email", responses=auth_email)
async def verify_email_token(
        token: str = Form(...),
        db: AsyncSession = Depends(get_db)):
  try:
    return await EmailService.verify_email(token, db)
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)