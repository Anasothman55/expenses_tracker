from typing import Dict, Union, TypedDict
from enum import Enum

class HTTPMethod(str, Enum):
  GET = "GET"
  POST = "POST"
  PUT = "PUT"
  DELETE = "DELETE"
  PATCH = "PATCH"

class Route(TypedDict):
  method: HTTPMethod
  path: str
  path_params: str | None

class CurrenciesRoutes(TypedDict):
  get: Route
  post: Route

class UserRoutes(TypedDict):
  me: Route

class AuthRoutes(TypedDict):
  register: Route
  verify: Route
  login: Route
  refresh_token: Route
  logout: Route
  forgot_password: Route
  reset_password_verify: Route
  reset_password: Route

class V1Routes(TypedDict):
  auth: AuthRoutes
  user: UserRoutes
  currencies: CurrenciesRoutes

class APIRoutes(TypedDict):
  v1: V1Routes

APITree = Dict[str, Union[Route, 'APITree']]

api_tree: APIRoutes = {
  "v1": {
    "auth": {
      "register": {
        "method": HTTPMethod.POST,
        "path": "api/v1/auth/register",
        "path_params": None,
      },
      "verify": {
        "method": HTTPMethod.GET,
        "path": "api/v1/auth/verify",
        "path_params": "verify_token",
      },
      "login": {
        "method": HTTPMethod.POST,
        "path": "api/v1/auth/login",
        "path_params": None,
      },
      "refresh_token": {
        "method": HTTPMethod.GET,
        "path": "api/v1/auth/refresh-token",
        "path_params": None,
      },
      "logout": {
        "method": HTTPMethod.GET,
        "path": "api/v1/auth/logout",
        "path_params": None,
      },
      "forgot_password": {
        "method": HTTPMethod.POST,
        "path": "api/v1/auth/forgot-password",
        "path_params": None,
      },
      "reset_password_verify": {
        "method": HTTPMethod.POST,
        "path": "api/v1/auth/reset-password-verify",
        "path_params": None,
      },
      "reset_password": {
        "method": HTTPMethod.PUT,
        "path": "api/v1/auth/reset-password",
        "path_params": None,
      },
    },
    "user": {
      "me": {
        "method": HTTPMethod.GET,
        "path": "api/v1/user/me",
        "path_params": None,
      }
    },
    "currencies": {
      "get": {
        "method": HTTPMethod.GET,
        "path": "api/v1/currencies",
        "path_params": None,
      },
      "post": {
        "method": HTTPMethod.POST,
        "path": "api/v1/currencies",
        "path_params": None,
      }
    }
  }
}

