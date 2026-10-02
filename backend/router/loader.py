from fastapi import APIRouter
from router.endpoints.auth import router as auth_router
from router.endpoints.courses import router as course_router

router = APIRouter(prefix="/api/v1")

router.include_router(auth_router)
router.include_router(course_router)
