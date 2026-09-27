import enum
from datetime import datetime

from core.database import Base
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy import (
    Enum as SAEnum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class TimestampMixin(CreatedAtMixin):
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
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
        SAEnum(
            UserRole,
            name="user_role",
            native_enum=False,
            length=16,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=UserRole.STUDENT.value,
    )

    courses_owned = relationship(
        "Course",
        back_populates="owner",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    courses_joined = relationship(
        "Course",
        secondary="members",
        back_populates="members",
    )

    __table_args__ = (Index("ix_users_active_role", "is_active", "role"),)


class CourseEntryType(str, enum.Enum):
    CLOSED = "closed"
    REQUEST = "request"
    OPEN = "open"


class Course(Base, TimestampMixin):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    llm_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    owner = relationship(
        "User",
        back_populates="courses_owned",
        passive_deletes=True,
    )

    restriction_status: Mapped[str] = mapped_column(
        SAEnum(
            CourseEntryType,
            name="course_entry_type",
            native_enum=False,
            length=16,
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        default=CourseEntryType.OPEN.value,
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    members = relationship(
        "User",
        secondary="members",
        back_populates="courses_joined",
    )

    __table_args__ = (
        Index("ix_courses_active_id", "is_active", "id"),
        UniqueConstraint("owner_id", "name", name="uq_course_owner_name"),
    )


class Member(Base, CreatedAtMixin):
    __tablename__ = "members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))

    __table_args__ = (
        UniqueConstraint("user_id", "course_id", name="uq_members_user_course"),
    )
