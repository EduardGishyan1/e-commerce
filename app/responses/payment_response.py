from app.responses.common import default_responses, status


payment_post_response = {
  **default_responses,
  status.HTTP_201_CREATED: {
    "description": "Payment session created successfully.",
    "content": {
      "application/json": {
        "example": {
          "session_id": "session_12345",
          "currency": "USD",
          "order_id": 1,
          "message": "Payment session created successfully."
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
              "field": "currency",
              "message": "Currency is required.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  },
  status.HTTP_404_NOT_FOUND: {
    "description": "Order not found.",
    "content": {
      "application/json": {
        "example": {
          "message": "Order not found."
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
              "field": "order_id",
              "message": "Order ID must be a positive integer.",
              "type": "value_error.number"
            }
          ]
        }
      }
    }
  }
}

stripe_webhook_response = {
  status.HTTP_200_OK: {
    "description": "Webhook processed successfully.",
    "content": {
      "application/json": {
        "example": {
          "message": "Webhook processed successfully.",
          "event_id": "evt_123456789",
          "event_type": "payment_intent.succeeded"
        }
      }
    }
  },
  status.HTTP_400_BAD_REQUEST: {
    "description": "Invalid webhook payload.",
    "content": {
      "application/json": {
        "example": {
          "message": "Invalid webhook payload.",
          "errors": [
            {
              "field": "payload",
              "message": "Payload is missing required fields.",
              "type": "value_error.missing"
            }
          ]
        }
      }
    }
  },
  status.HTTP_401_UNAUTHORIZED: {
    "description": "Unauthorized webhook request.",
    "content": {
      "application/json": {
        "example": {
          "message": "Unauthorized webhook request."
        }
      }
    }
  },
  status.HTTP_422_UNPROCESSABLE_ENTITY: {
    "description": "Validation error.",
    "content": {
      "application/json": {
        "example": {
          "message": "Validation failed. Please check the webhook payload.",
          "errors": [
            {
              "field": "event_type",
              "message": "Invalid event type.",
              "type": "value_error.event_type"
            }
          ]
        }
      }
    }
  }
}