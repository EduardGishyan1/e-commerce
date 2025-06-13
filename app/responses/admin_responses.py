from fastapi import status


default_responses = {
  status.HTTP_500_INTERNAL_SERVER_ERROR: {
    "description": "Internal Server Error",
    "content": {
      "application/json": {
        "example": {
          "detail": "Something went wrong"
        }
      }
    }
  },
  status.HTTP_401_UNAUTHORIZED: {
    "description": "Error: Unauthorized",
    "content": {
      "application/json": {
        "example": {
          "detail": "Not authenticated"
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Not found",
    "content": {
      "application/json": {
        "example": {
          "detail": "Data not found"
        }
      }
    }
  }
}

for_review = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "id": 0,
          "rating": 5,
          "created_at": "2025-01-25T11:41:20.901381",
          "user_id": 0,
          "product_id": 0,
          "content": "very good",
          "is_flagged": True
        }
      }
    }
  }
}

for_resolve_review = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "detail": "Review resolved successfully"
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Bad request",
    "content": {
      "application/json": {
        "example": {
          "detail": 'Review is already resolved'
        }
      }
    }
  }
}

for_user = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
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
  }
}

for_order = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
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
  }
}

for_sales = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "total_revenue": 1000,
          "total_sales": 100,
          "top_selling_products": [
            {
              "product_id": 1,
              "sales_count": 100
            },
            {
              "product_id": 2,
              "sales_count": 100
            }
          ]
        }
      }
    }
  }
}

for_analytics = {**default_responses,
  status.HTTP_200_OK: {
    "description": "Success",
    "content": {
      "application/json": {
        "example": {
          "most_active_user": {
            "username": "string",
            "name": "string",
            "surname": "string",
            "email": "string@example.com",
            "order_count": 1
          },
          "most_viewed_product": {
            "name": "Product A",
            "description": "Description for Product A",
            "price": 9.99,
            "category": {
              "type": "Category 1"
            },
            "created_at": "2025-01-25T12:10:19",
            "is_active": True,
            "image_url": "https://example.com/imageA.jpg",
            "id": 1,
            "stock": 1,
            "vendor_id": 1,
            "updated_at": "2025-01-25T12:10:19",
            "is_deleted": False,
            "view_count": 100
          }
        }
      }
    }
  }
}