from app.responses.common import default_responses, status


order_responses = {
  status.HTTP_401_UNAUTHORIZED: {
    "description": "User is unauthorized",
    "content": {
      "application/json": {
        "example": {
          "error": "Unauthorized",
          "message": "You must provide a valid API key to access this resource."
        }
      }
    }
  },
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Order created successfully",
    "content": {
      "application/json": {
        "example": {
          "id": 1,
          "user_id": 1,
          "total_amount": 4.0,
          "status": "paid",
          "created_at": "2025-01-01T14:00",
          "updated_at": "2025-04-04T16:40"
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
          "message": "The provided order data is not valid"
        }
      }
    }
  },
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "message": "Order was successfully created"
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Order is not found",
    "content": {
      "application/json": {
        "example": {
          "error": "Not found",
          "message": "Order is not found"
        }
      }
    }
  }
}