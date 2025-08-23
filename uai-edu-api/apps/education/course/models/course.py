from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.education.zone.models import UaiEduZone
from apps.education.category.models import UaiEduCategory
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text
from .m2m import uai_edu_course_zones, uai_edu_course_categories


class UaiEduCourse(BaseModel):
    __tablename__ = "uai_edu_course"
    __table_args__ = ({'comment': '课程信息表'})

    course_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="课程名称")
    course_cover: Mapped[str] = mapped_column(String(200), nullable=False, comment="课程封面")
    course_desc: Mapped[str | None] = mapped_column(Text, comment="课程描述")
    lecturer: Mapped[int | None] = mapped_column(Integer, comment="授课教师")
    instructor: Mapped[int | None] = mapped_column(Integer, comment="指导教师")

    zones: Mapped[set[UaiEduZone]] = relationship(secondary=uai_edu_course_zones)
    categories: Mapped[set[UaiEduCategory]] = relationship(secondary=uai_edu_course_categories)
