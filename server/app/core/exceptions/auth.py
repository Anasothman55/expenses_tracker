from fastapi import HTTPException, status


from app.core.exceptions.handler import AppException
from app.shared.utils.ctype import ExceptionDetails


class AuthException(AppException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Authentication failed"
  error_code = "AUTH_ERROR"

class InvalidCredentialsException(AuthException):
  message = "Invalid email or password"
  error_code = "INVALID_CREDENTIALS"


class InActiveUserException(AuthException):
  status_code = status.HTTP_403_FORBIDDEN
  message = "Inactive user"
  error_code = "INACTIVE_USER"

class TokenIsMissingException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Authentication credentials were not provided."
  error_code = "TOKEN_IS_MISSING"

class EmailNotVerifiedException(AuthException):
  status_code = status.HTTP_403_FORBIDDEN
  message = "Email address is not verified"
  error_code = "EMAIL_NOT_VERIFIED"

class RefreshTokenExpiredException(AuthException):
  message = "Refresh token has expired"
  error_code = "REFRESH_TOKEN_EXPIRED"

class EmailVerifyTokenException(AuthException):
  message = "Invalid email verification token"
  error_code = "INVALID_EMAIL_VERIFY_TOKEN"

class EmailVerifyTokenExpiredException(AuthException):
  message = "Email verification token has expired"
  error_code = "EMAIL_VERIFY_TOKEN_EXPIRED"

class RegistrationConflictException(AppException):
  status_code = status.HTTP_409_CONFLICT
  message = "Registration validation failed"
  error_code = "REGISTRATION_CONFLICT"

class AccountDisabledException(AuthException):
  status_code = status.HTTP_403_FORBIDDEN
  message = "Account has been disabled"
  error_code = "ACCOUNT_DISABLED"

class UnauthorizedException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  error_code = "UNAUTHORIZED"

class InvalidResetIdException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Invalid reset id"
  error_code = "INVALID_RESET_ID"

class InvalidOtpException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Invalid otp"
  error_code = "INVALID_OTP"

class InvalidPasswordResetTokenException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Invalid password reset verification token"
  error_code = "INVALID_PASSWORD_RESET_TOKEN"

class SamePasswordException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Same password reset value"
  error_code = "SAME_PASSWORD"

class ExpiredPasswordResetTokenException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Password reset verification token has expired"
  error_code = "PASSWORD_RESET_TOKEN_EXPIRED"

class JoseException(AuthException):
  status_code = status.HTTP_401_UNAUTHORIZED
  message = "Authentication failed"
  error_code = "JOSE_ERROR"

class TokenReusedException(JoseException):
  message = "Authentication failed"
  error_code = "TOKEN_REUSED"

class RefreshTokenBlacklistedException(JoseException):
  message = "Refresh token is no longer valid"
  error_code = "REFRESH_TOKEN_BLACKLISTED"

class InvalidTokenException(JoseException):
  message = "Invalid token"
  error_code = "INVALID_TOKEN"

class InvalidTokenSessionIdException(JoseException):
  message = "Invalid session id"
  error_code = "INVALID_TOKEN_SESSION_ID"

class TokenSignatureException(JoseException):
  message = "Token signature is invalid"
  error_code = "INVALID_TOKEN_SIGNATURE"

class MissingTokenClaimException(JoseException):
  message = "Required token claim is missing"
  error_code = "MISSING_TOKEN_CLAIM"

class InvalidTokenClaimException(JoseException):
  message = "Token claim is invalid"
  error_code = "INVALID_TOKEN_CLAIM"

class UnsupportedTokenAlgorithmException(JoseException):
  message = "Token algorithm is not supported"
  error_code = "UNSUPPORTED_TOKEN_ALGORITHM"

class ExpiredTokenException(JoseException):
  message = "Token has expired"
  error_code = "TOKEN_EXPIRED"

class InvalidTokenTypeException(JoseException):
  message = "Invalid token type"
  error_code = "INVALID_TOKEN_TYPE"

