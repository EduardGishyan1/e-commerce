from app.responses.common import default_responses, status


review_post_response = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Review created successfully.",
    "content": {
      "application/json": {
        "example": {
          "review_id": 123,
          "content": "This product is great!",
          "rating": 5,
          "user_id": 1,
          "product_id": 1,
          "message": "Review created successfully."
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Invalid request.",
    "content": {
      "application/json": {
        "example": {
          "message": "Invalid request. Please check your input.",
          "errors": [
            {
              "field": "rating",
              "message": "Rating must be between 1 and 5.",
              "type": "value_error.rating"
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "User or product not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "User or product not found."
        }
      }
    }
  },
  status.HTTP_422_UNPROCESSABLE_ENTITY: {
    "description": "Validation error.",
    "content": {
      "application/json": {
        "example": {
          "message": "Validation failed. Please correct the following errors and try again.",
          "errors": [
            {
              "field": "content",
              "message": "Content is required.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  }
}

review_put_response = {
  status.HTTP_200_OK: {
    "description": "Review updated successfully.",
    "content": {
      "application/json": {
        "example": {
          "review_id": 123,
          "content": "Updated review content.",
          "rating": 4,
          "user_id": 1,
          "product_id": 1,
          "message": "Review updated successfully."
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Invalid request.",
    "content": {
      "application/json": {
        "example": {
          "message": "Invalid request. Please check your input.",
          "errors": [
            {
              "field": "rating",
              "message": "Rating must be between 1 and 5.",
              "type": "value_error.rating"
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Review not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Review not found."
        }
      }
    }
  },
  status.HTTP_422_UNPROCESSABLE_ENTITY: {
    "description": "Validation error.",
    "content": {
      "application/json": {
        "example": {
          "message": "Validation failed. Please correct the following errors and try again.",
          "errors": [
            {
              "field": "content",
              "message": "Content is required.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  }
}

review_delete_response = {
  status.HTTP_204_NO_CONTENT: {
    "description": "Review deleted successfully.",
    "content": None
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Review not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Review not found."
        }
      }
    }
  }
}