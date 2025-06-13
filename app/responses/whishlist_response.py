from app.responses.common import default_responses, status


wishlist_post_response = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Wishlist created successfully.",
    "content": {
      "application/json": {
        "example": {
          "wishlist_id": 123,
          "product_id": 1,
          "message": "Wishlist created successfully."
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
              "field": "product_id",
              "message": "Product ID is required.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Product not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Product not found."
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
              "field": "product_id",
              "message": "Product ID must be a positive integer.",
              "type": "value_error.number"
            }
          ]
        }
      }
    }
  }
}

delete_wishlist_response = {
  status.HTTP_204_NO_CONTENT: {
    "description": "Wishlist item deleted successfully.",
    "content": None
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Wishlist item not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Wishlist item not found."
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
              "field": "product_id",
              "message": "Invalid product ID format.",
              "type": "value_error.id"
            }
          ]
        }
      }
    }
  }
}

delete_all_wishlists_response = {
  status.HTTP_204_NO_CONTENT: {
    "description": "All wishlist items deleted successfully.",
    "content": None
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Invalid request.",
    "content": {
      "application/json": {
        "example": {
          "message": "Invalid request. Please check your input."
        }
      }
    }
  }
}