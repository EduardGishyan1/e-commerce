from fastapi import status


default_responses = {
  status.HTTP_401_UNAUTHORIZED: {
    "description": 
      "Unauthorized access",
        "content": {
          "application/json": {
            "example": {
              "detail": "Invalid email or password"
            }
        }
      }
    },
  status.HTTP_403_FORBIDDEN : {
    "description" : 
      "Forbidden",
        "content": {
          "application/json": {
            "example": {
              "detail": "Need Admin access"
            }
          }
      }
  },
  status.HTTP_500_INTERNAL_SERVER_ERROR: {
    "description": 
      "Interal Server Error",
        "content": {
          "application/json": {
            "example": {
              "detail": "Something went wrong"
        }
      }
    }
  }
}