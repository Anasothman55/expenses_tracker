from fastapi import APIRouter

from .auth.api import auth_route
from .user.api import user_route
from .currencies.api import currencies_route
from .category_group.api import category_group_route
from .categories.api import categories_route
from .transactions.api import transactions_route

router_v1 = APIRouter(
  prefix='/v1'
)


router_v1.include_router(auth_route, prefix='/auth')
router_v1.include_router(user_route, prefix='/user')
router_v1.include_router(currencies_route, prefix='/currencies')
router_v1.include_router(category_group_route, prefix='/category-group')
router_v1.include_router(categories_route, prefix='/categories')
router_v1.include_router(transactions_route, prefix='/transactions')