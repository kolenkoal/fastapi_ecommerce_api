from functools import wraps

from src.database import async_session_factory


def manage_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_factory() as session:
            if "session" not in kwargs:
                kwargs["session"] = session
            return await func(*args, **kwargs)

    return wrapper
