from uuid import UUID

from loguru import logger
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only, DeclarativeMeta, DeclarativeBase
from sqlalchemy.orm.interfaces import ORMOption
from sqlalchemy import select, Select, func, inspect, column
from sqlalchemy.exc import SQLAlchemyError

from rich import print

from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi.encoders import jsonable_encoder

from typing import Any, Sequence, Type, Callable, TypeVar, Generic, Self, List, Iterable, Literal
from functools import wraps

from app.core.exceptions.sql import NotFoundException, SQLException
from app.shared.utils.ctype import ExceptionDetails


def database_exception_wrap(fn: Callable):
  @wraps(fn)
  async def wrapper(self, *args, **kwargs):
    try:
      return await fn(self, *args, **kwargs)
    except NotFoundException:
      raise
    except SQLAlchemyError as e:
      await self.db.rollback()
      err = str(e)
      raise SQLException(
        detail=[jsonable_encoder(err)],
        message= err.split(":")[1].strip().split("[SQL")[0].strip() if 'psycopg' in err else "An error occurred while processing the database operation."
      )
    except Exception as e:
      await self.db.rollback()
      raise e
  return wrapper




T = TypeVar('T', bound=DeclarativeBase)
S = TypeVar('S', bound=BaseModel)

class ModelRepository(Generic[T]):

  def __init__(self, db: AsyncSession, model: Type[T]) :
    self.db: AsyncSession = db
    self.model: Type[T] = model

  async def __aenter__(self)-> Self:
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    if exc_type:
      await self.db.rollback()
    else:
      await self.db.commit()

  @database_exception_wrap
  async def get_one(
      self,
      field: str,
      value: Any,
      options: Iterable[ORMOption] = [], # type ignore
      include_deleted: bool = False,
      select_stmt: Select | None = None,
  ) -> T :

    stmt = select_stmt if select_stmt else  select(self.model)
    stmt = stmt.where(getattr(self.model, field) == value).options(*options)

    if not include_deleted:
      stmt = stmt.where(self.model.deleted_at.is_(None))

    if instance := (await self.db.execute(stmt)).scalar_one_or_none():
      return instance
    else:
      raise NotFoundException(
        #message=f"Value {value} not found in {self.model}: {field}",
        detail=[
          ExceptionDetails(
            loc=[field],
            input=value,
            msg=f'Value {value} not found in {self.model}: {field}',
            type=f'type_error.{field}'
          )
        ]
      )

  @database_exception_wrap
  async def get_count(self) -> Any:
    pk = inspect(self.model).primary_key[0]
    return (
      await self.db.execute(
        select(
          func.count(pk)
        )
      )
    ).scalar()

  @database_exception_wrap
  async def get_all(
      self,
      is_pagination: bool,
      include_deleted: bool,
      select_stmt: Select[tuple[T]] | None = None,
      params: Params | None = None,
  )-> Sequence[T] | Any:

    stmt = select_stmt if select_stmt is not None else select(self.model)

    if not include_deleted:
      stmt = stmt.where(self.model.deleted_at.is_(None))

    logger.info(stmt)
    if is_pagination:
      return await paginate(self.db,stmt, params, unique=False)
    return (await self.db.execute(stmt)).scalars().all()

  @database_exception_wrap
  async def create(self, body: S | dict) -> T:
    if isinstance(body, dict):
      instance = self.model(**body)
    else:
      instance = self.model(**body.model_dump(exclude_unset=True))
    self.db.add(instance)
    await self.db.flush()
    await self.db.refresh(instance)
    return instance


  @database_exception_wrap
  async def update(self, uid: UUID | None = None, body: S | dict | None = None, obj_instance: T | None = None) -> T:
    """ for update model but as note never update deleted_at"""
    if obj_instance is None:
      instance = await self.get_one("uid", uid)
      data = body if type(body) is dict else body.model_dump(exclude_unset=True)
      for key, value in data.items():
        if hasattr(instance, key):
          setattr(instance, key, value)
    else:
      instance = obj_instance
    await self.db.flush()
    await self.db.refresh(instance)
    return instance


  @database_exception_wrap
  async def delete(self, uid: UUID, delete_type: Literal['soft_delete', 'internal_delete'] | None = 'soft_delete', obj_instance: T | None = None) -> None:
    hard_delete: bool = True if delete_type == 'internal_delete' else False
    instance = await self.get_one("uid", uid, include_deleted=hard_delete) if obj_instance is None else obj_instance

    if delete_type == 'soft_delete':
      await self.db.commit()
    else:
      await self.db.delete(instance)
    await self.db.flush()


class UnitOfWork:

  def __init__(self, db: AsyncSession):
    self.db = db

  async def __aenter__(self)-> Self:
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    if exc_type:
      await self.db.rollback()
    else:
      await self.db.commit()

  def repo(self, model: Type[T]) -> ModelRepository[T]:
    return ModelRepository(self.db, model)



