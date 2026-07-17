from fastapi import status


from app.core.exceptions.handler import AppException


class SQLException(AppException):
  error_code = "SQLException"
  message = "An error accorded in the database please try again"

class NotFoundException(AppException):
  status_code = status.HTTP_404_NOT_FOUND
  message = "The requested resource could not be found"
  error_code = "NOT_FOUND"












