class EmailConstants:
  @staticmethod
  def email_verify_subject():
    return "Verify Your Email Address"

  @staticmethod
  def email_verify_body(token: str, frontend_verification_url: str):
    return f"""
        <strong>Hello</strong>
        
        <p>Thank you for signing up with e_Commerce. To complete your registration, we need to verify your email address.</p>
        <p>Please click the link below to verify your email:</p>
        <p>This is your verification code: <b>{token}</b></p>
        <p><a href="{frontend_verification_url}">Verify Email</a></p>
        <p>If you did not request this, please ignore this email.</p>
        <p>Thank you python odyssey, e_Commerce Team</p>        
        """

  @staticmethod
  def registration_body():
    return "<p>Thank you for registering with us!</p>"

  @staticmethod
  def registration_subject():
    return "Verify Your Email"

  @staticmethod
  def registration_message_email(verification_link: str, token: str):
    return f"""
          <html>
          <body>
              <p>Thank you for registering. Please verify your email by clicking the link below:</p>
              <a href="{verification_link}">Verify Email</a>
          </body>
          </html>
          """

  @staticmethod
  def update_subject():
    return "Your Profile Has Been Updated"

  @staticmethod
  def update_body():
    return ("<p>Your profile information has been successfully updated. If you didn't make this change, "
            "please contact our support team immediately.</p>")

  @staticmethod
  def deletion_subject():
    return "Your Account Has Been Deleted"

  @staticmethod
  def deletion_body():
    return ("<p>Your account has been successfully deleted. If this was not done by you, "
            "please contact our support team immediately.</p>")

  @staticmethod
  def order_placement_subject():
    return "Your Order Has Been Placed"

  @staticmethod
  def change_password():
    return "e_Commerce Team."

  @staticmethod
  def change_password_body():
    return "<p>Your password has been changed successfully.</p>"

  @staticmethod
  def order_placement_body():
    return "<p>Thank you for your order! You will receive further updates as your order is processed.</p>"

  @staticmethod
  def payment_confirmation_subject():
    return "Payment Confirmation"

  @staticmethod
  def payment_confirmation_body():
    return "<p>We have received your payment successfully! Thank you for your purchase.</p>"

  @staticmethod
  def password_reset_subject():
    return "Password Reset Request"

  @staticmethod
  def password_reset_body(token, reset_link: str):
    return f"""
            <p>We received a request to reset your password. 
            <p>Here is your code:</p>
            <p><b>{token}</b></p>
            Click the link below to reset your password:</p>
            <p><a href="{reset_link}">Reset Password</a></p>
            <p>If you did not request this, please ignore this email or contact support.</p>
            """