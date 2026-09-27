import enum
from datetime import datetime

from core.database import Base
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


class TimestampMixin(CreatedAtMixin):
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    needs_password_change: Mapped[bool] = mapped_column(Boolean, default=False)

    role: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="student",
    )

    __table_args__ = (
        Index("ix_users_active_role", "is_active", "role"),
        CheckConstraint(
            f"role IN ({','.join(repr(r.value) for r in UserRole)})",
            name="ck_users_role_valid",
        ),
    )


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship(back_populates="owned_courses")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (Index("ix_courses_active_id", "is_active", "id"),)


class Members(Base, CreatedAtMixin):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))

    __table_args__ = (
        Index("ix_members_user_id_course_id", "user_id", "course_id"),
        UniqueConstraint("user_id", "course_id", name="uix_members_user_id_course_id"),
    )
