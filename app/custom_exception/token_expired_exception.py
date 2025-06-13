from fastapi import HTTPException, status

class TokenExpires(HTTPException):
  def __init__(self):
    super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Token expired", 
                    headers={"WWW-Authenticate": "Bearer"})