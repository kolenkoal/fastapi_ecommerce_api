from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.dao import BaseDAO
from src.database import async_session_factory
from src.products.categories.models import ProductCategory


class ProductCategoryDAO(BaseDAO):
    model = ProductCategory

    @classmethod
    async def find_all(cls):
        async with async_session_factory() as session:
            query = select(cls.model).order_by(cls.model.id)

            result = await session.execute(query)

            values = result.scalars().all()

            return values

    @classmethod
    async def find_by_id(
        cls,
        model_id,
    ) -> model:
        async with async_session_factory() as session:
            query = (
                select(cls.model)
                .options(joinedload(cls.model.children_categories))
                .filter_by(id=model_id)
            )

            result = await session.execute(query)

            return result.unique().mappings().one_or_none()["ProductCategory"]
