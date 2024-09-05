from .. import dependencies as dep
from fastapi import APIRouter
from ..models import students
import sqlalchemy as sql
from ..database import Student

router = APIRouter(prefix="/students")


@router.get("/{student_id}", response_model=students.Out)
async def get_student_by_id(student: dep.model.Student, db: dep.DB):
    return student


@router.post("/", response_model=students.Out)
async def create_student(schema: students.In, db: dep.DB):
    query = sql.insert(Student).values(**schema.model_dump()).returning(Student)
    result = await db.execute(query)
    return result.scalar_one()


# @router.patch("/{student_id}")

#
