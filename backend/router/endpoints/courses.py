import json
from typing import List

from core.database import get_db
from core.security import get_current_user, require_role
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from models.database import Course, CourseEntryType, Member, MemberRequests, User
from schemas.api import CourseJoin, CourseOut, Feedback
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

router = APIRouter(prefix="/courses")


@router.get("/list/available", response_model=list[CourseOut], status_code=200)
def list_courses_available(
    user: User = Depends(require_role("*")), db: Session = Depends(get_db)
):
    joined_ids = select(Member.course_id).where(Member.user_id == user.id)

    return (
        db.query(Course)
        .filter(
            Course.is_active.is_(True),
            Course.id.not_in(joined_ids),
        )
        .all()
    )


@router.get("/list", response_model=list[CourseOut], status_code=200)
def list_courses_joined(
    user: User = Depends(require_role("*")), db: Session = Depends(get_db)
):
    db_user = db.get(User, user.id)
    return db_user.courses_joined


@router.post("/join", response_model=Feedback, status_code=200)
def join_course(
    payload: CourseJoin,
    user: User = Depends(require_role("*")),
    db: Session = Depends(get_db),
):
    db_course = db.get(Course, payload.course_id)

    if db_course.restriction_status == CourseEntryType.CLOSED.value:
        raise HTTPException(400, "This course has disabled the ability to join")

    if db_course.restriction_status == CourseEntryType.REQUEST.value:
        request_entry = MemberRequests(
            user_id=user.id, course_id=payload.course_id, message=payload.message
        )

        try:
            db.add(request_entry)
            db.commit()
            db.refresh(request_entry)
            return Feedback(
                status="ok", message="Sent course join application successfully"
            )
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(400, "Submiting course join application failed")

    db_user = db.get(User, user.id)

    if db_course in db_user.courses_joined:
        raise HTTPException(400, "Already a member of this course")

    member_entry = Member(user_id=user.id, course_id=payload.course_id)

    try:
        db.add(member_entry)
        db.commit()
        db.refresh(member_entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Joining course failed")

    return Feedback(status="ok", message="Joined course successfully")
