from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.models import str2000, uuidpk


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[uuidpk]
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    profile_image: Mapped[str] = mapped_column(
        nullable=False, default="default.webp"
    )
    bio: Mapped[str2000] = mapped_column(nullable=True)

    user = relationship("User", back_populates="profile")
