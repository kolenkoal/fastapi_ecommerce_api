from uuid import UUID


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: UUID):
        pass
