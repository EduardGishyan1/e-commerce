from app.responses.common import default_responses, status


user_responses = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "User created successfully",
    "content": {
      "application/json": {
        "example": {
          "id": 101,
          "name": "John Doe",
          "email": "johndoe@example.com",
          "role": "admin",
          "created_at": "2025-05-15T10:00:00",
          "updated_at": "2025-05-15T10:00:00"
        }
      }
    }
  },
  status.HTTP_200_OK: {
    "description": "User details retrieved successfully",
    "content": {
      "application/json": {
        "example": {
          "id": 101,
          "name": "John Doe",
          "email": "johndoe@example.com",
          "role": "admin",
          "created_at": "2025-05-15T10:00:00",
          "updated_at": "2025-05-15T10:00:00"
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Invalid user data",
    "content": {
      "application/json": {
        "example": {
          "error": "Invalid input",
          "message": "One or more fields are invalid. Please check your data and try again."
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "User not found",
    "content": {
      "application/json": {
        "example": {
          "error": "Not found",
          "message": "The user with the specified ID does not exist."
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
          "message": "You do not have permission to access this resource."
        }
      }
    }
  },
  status.HTTP_403_FORBIDDEN: {
    "description": "Access forbidden",
    "content": {
      "application/json": {
        "example": {
          "error": "Forbidden",
          "message": "You do not have the required permissions to perform this action."
        }
      }
    }
  }
}