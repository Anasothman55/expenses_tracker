from datetime import datetime
from uuid import UUID

from sqladmin import ModelView
from sqladmin.filters import OperationColumnFilter
from wtforms import PasswordField
from fastapi import Request

from src.infrastructure.db.models import CurrenciesModel
from src.core.security.password_hashing import password_hash
from src.infrastructure.db.models import UserModel


class CurrencyView(ModelView, model=CurrenciesModel):
  can_create = True
  can_edit = True
  can_delete = True
  can_view_details = True

  column_list = [
    CurrenciesModel.uid,
    CurrenciesModel.name,
    CurrenciesModel.code,
    CurrenciesModel.symbol,
    CurrenciesModel.created_at,
    CurrenciesModel.updated_at,
    CurrenciesModel.deleted_at,
  ]

  column_details_list = [
    CurrenciesModel.uid,
    CurrenciesModel.name,
    CurrenciesModel.code,
    CurrenciesModel.symbol,
    CurrenciesModel.created_at,
    CurrenciesModel.updated_at,
    CurrenciesModel.deleted_at,
  ]

  form_columns = [
    CurrenciesModel.name,
    CurrenciesModel.code,
    CurrenciesModel.symbol,
  ]

  column_type_formatters = {
    type(None): lambda x: 'Empty',
    str: lambda x: x[:10],
    #UUID: lambda x: 'UUID',
    datetime: lambda x: datetime.strftime(x,"%d-%m-%Y %I:%M %p"),

  }
  column_type_formatters_detail = {
    type(None): lambda x: 'Null',
    str: lambda x: x
  }

class UserView(ModelView, model=UserModel):

  can_create = True
  can_edit = True
  can_delete = True
  can_view_details = True

  column_list = [
    UserModel.uid,
    UserModel.email,
    UserModel.username,
    UserModel.is_active,
    UserModel.is_verified,
    UserModel.failed_login_attempts,
    UserModel.last_login_at,
    UserModel.password_changed_at,
    UserModel.user_currencies,
    UserModel.created_at,
    UserModel.updated_at,
    UserModel.deleted_at,
  ]

  column_details_list = [
    UserModel.uid,
    UserModel.email,
    UserModel.username,
    UserModel.is_active,
    UserModel.is_verified,
    UserModel.failed_login_attempts,
    UserModel.last_login_at,
    UserModel.password_changed_at,
    UserModel.currency,
    UserModel.created_at,
    UserModel.updated_at,
    UserModel.deleted_at,
  ]


  # Fields in the create form

  form_columns = [
    UserModel.email,
    UserModel.username,
    UserModel.encoded_password,
    UserModel.is_active,
    UserModel.is_verified,
    UserModel.currency,
  ]

  async def on_model_change(
      self,
      data: dict,
      model: UserModel,
      is_created: bool,
      request: Request,
  ) -> None:

    if is_created:
      password = data.get("encoded_password")

      if password:
        data["encoded_password"] = password_hash(password)

  form_overrides = {
    "encoded_password": PasswordField,
  }

  form_widget_args = {
    "username": {
      "placeholder": "Enter username",
    },
    "email": {
      "placeholder": "user@example.com",
    },
  }

  column_filters = [
    OperationColumnFilter(UserModel.email),
    OperationColumnFilter(UserModel.username),
    OperationColumnFilter(UserModel.is_active),
    OperationColumnFilter(UserModel.is_verified),
    OperationColumnFilter(UserModel.failed_login_attempts),
    OperationColumnFilter(UserModel.last_login_at),
    OperationColumnFilter(UserModel.password_changed_at),
    OperationColumnFilter(UserModel.user_currencies),
    OperationColumnFilter(UserModel.created_at),
    OperationColumnFilter(UserModel.updated_at),
    OperationColumnFilter(UserModel.deleted_at),
  ]

  column_type_formatters = {
    type(None): lambda x: 'Empty',
    str: lambda x: x[:10],
    UUID: lambda x: 'UUID',
    datetime: lambda x: datetime.strftime(x,"%d-%m-%Y %I:%M %p"),
  }
  column_type_formatters_detail = {
    type(None): lambda x: 'Null',
    str: lambda x: x
  }
