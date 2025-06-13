from app.responses.common import default_responses, status


cart_item_post_response = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Cart item added successfully.",
    "content": {
      "application/json": {
        "example": {
          "id": 456,
          "product_id": 123,
          "quantity": 2,
          "message": "Cart item added successfully."
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    **default_responses,
    "description": "Invalid request.",
    "content": {
      "application/json": {
        "example": {
          "message": "Invalid request. Please check your input.",
          "errors": [
            {
              "field": "quantity",
              "message": "Quantity must be greater than 0.",
              "type": "value_error.quantity"
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    **default_responses,
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
              "message": "Product ID is required.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  }
}

delete_response = {
  **default_responses,
  status.HTTP_200_OK: {
    "description": "Resource deleted successfully.",
    "content": {
      "application/json": {
        "example": {
          "message": "Resource deleted successfully.",
          "cart_item_1id": 123
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Cart item not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Cart item not found."
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
              "field": "id",
              "message": "Invalid ID format.",
              "type": "value_error.id"
            }
          ]
        }
      }
    }
  }
}