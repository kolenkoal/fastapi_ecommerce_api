from sqlalchemy import or_, select

from src.users.models import Role
from src.utils.session import manage_session


@manage_session
async def has_permission(user, session=None):
    get_privileged_roles_query = select(Role.id).where(
        or_(
            Role.name == "admin",
            Role.name == "manager",
        )
    )
    privileged_roles = (
        (await session.execute(get_privileged_roles_query)).scalars().all()
    )

    if user.role_id in privileged_roles:
        return True
    return False
