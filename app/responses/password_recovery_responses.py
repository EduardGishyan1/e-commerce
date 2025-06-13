from app.responses.common import default_responses, status


password_recovery_responses = {
  **default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "message": "Password was successfully created"
        }
      }
    }
  },
  status.HTTP_401_UNAUTHORIZED: {
    "description": "Unauthorized access",
    "content": {
      "application/json": {
        "example": {
          "error": "Unauthorized",
          "message": "You are not authorized to initiate a password recovery. Please ensure you are logged in or provide valid credentials."
        }
      }
    }
  },
  status.HTTP_403_FORBIDDEN: {
    "description": "Forbidden",
    "content": {
      "application/json": {
        "example": {
          "error": "Forbidden",
          "message": "Token email does not match the user's email"
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Bad request, invalid input data",
    "content": {
      "application/json": {
        "example": {
          "error": "Invalid data",
          "message": "The provided data is not valid"
        }
      }
    }
  }
}