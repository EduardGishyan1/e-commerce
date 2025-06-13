from pathlib import Path
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status

from app.database.session import get_db
from app.utils.token import get_current_user
from app.services.password_recovery_service import InitPasswordRecovery
from app.schemas.user import PasswordInitiate, ChangePassword, SetNewPassword
from app.responses.password_recovery_responses import password_recovery_responses


router = APIRouter(prefix="/auth", tags=["Auth"])

BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "static")

@router.post("/initiate_password_recovery", responses=password_recovery_responses)
async def initiate_password_recovery(
        user: PasswordInitiate,
        db: AsyncSession = Depends(get_db)):
  try:
   response = await InitPasswordRecovery.initiate_password_recovery(user, db)
   return response
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/password_recovery", responses=password_recovery_responses)
async def do_password_recovery(
        email = Form(...),
        new_password = Form(...),
        repeat_password = Form(...),
        token = Form(...) ,
        db: AsyncSession = Depends(get_db)):
  try:
   userinfo = SetNewPassword(email=email, new_password=new_password,
                             repeat_password=repeat_password, token=token)
   message = await InitPasswordRecovery.do_password_recovery(userinfo, db)
   return message
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.get("/password_recovery")
async def password_recovery(request: Request):
  try:
    password_recovery_html = templates.TemplateResponse("password-recovery.html", {"request":request})
    return password_recovery_html
  except HTTPException as exc:
      return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
    return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)

@router.post("/change_password", responses=password_recovery_responses)
async def change_password(
        user_password: ChangePassword,
        current_user = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
  try:
      message = await InitPasswordRecovery.change_password(user_password, current_user, db)
      return message
  except HTTPException as exc:
    return JSONResponse(content={"message": str(exc)}, status_code=exc.status_code)
  except Exception as e:
      return {"message": str(e)}