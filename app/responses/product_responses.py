from fastapi import status


for_create = {
  status.HTTP_201_CREATED: {
    "description": "Product created successfully",
    "content": {
      "application/json": {
        "example": {
          "name": "product",
          "description": "this product is/consists of etc.",
          "price": 9.99,
          "stock": 99,
          "category": "category",
          "image_url": "www.example.com"
        }
      }
    }
  },
  status.HTTP_403_FORBIDDEN: {
    "description": "Forbidden",
    "content": {
      "application/json": {
        "example": {
          "detail": "You do not have permission to create a product. Need administrative or vendor access"
        }
      }
    }
  },
  status.HTTP_500_INTERNAL_SERVER_ERROR: {
    "description": "Internal Server Error",
    "content": {
      "application/json": {
        "example": {
          "detail": "Something went wrong"
        }
      }
    }
  }
}

for_get = {
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "name": "product",
          "description": "this product is/consists of etc.",
          "price": 9.99,
          "stock": 99,
          "category": "category",
          "image_url": "www.example.com"
        }
      }
    }
  },
  status.HTTP_403_FORBIDDEN: {
    "description": "Forbidden",
    "content": {
      "application/json": {
        "example": {
          "detail": "Need administrative or vendor access"
        }
      }
    }
  },
  status.HTTP_500_INTERNAL_SERVER_ERROR: {
    "description": "Internal Server Error",
    "content": {
      "application/json": {
        "example": {
          "detail": "Something went wrong"
        }
      }
    }
  }
}

delete_response = {
  status.HTTP_200_OK: {
    "description": "Product deleted successfully.",
    "content": {
      "application/json": {
        "example": {
          "product_id": 1,
          "role": "vendor",
          "message": "This product deleted from catalog."
        }
      }
    }
  },
  status.HTTP_403_FORBIDDEN: {
    "description": "Product not deleted.",
    "content": {
      "application/json": {
        "example": {
          "product_id": 1,
          "action": "Check your product_id or availability of product."
        }
      }
    }
  }
}

put_response = {
  status.HTTP_200_OK: {
    "description": "Product updated successfully.",
    "content": {
      "application/json": {
        "example": {
          "id": 123,
          "name": "Updated Name",
          "description": "Description updated",
          "stock": 1,
          "price": 66,
          "category": "Category updated",
          "image_url": "Image url updated",
          "message": "Product updated successfully."
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
              "message": "invalid input format.",
              "type": "value_error.product_id"
            }
          ]
        }
      }
    }
  }
}