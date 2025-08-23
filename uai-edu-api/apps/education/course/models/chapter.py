from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduCourseChapter(BaseModel):
    __tablename__ = "uai_edu_course_chapter"
    __table_args__ = ({'comment': '章节信息表'})

    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("uai_edu_course.id"), nullable=False, comment="课程ID")
    chapter_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="章节名称")
    chapter_desc: Mapped[str | None] = mapped_column(Text, comment="章节描述")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
