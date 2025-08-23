from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text, DECIMAL


class UaiEduCourseChapterLesson(BaseModel):
    __tablename__ = "uai_edu_course_chapter_lesson"
    __table_args__ = ({'comment': '课时信息表'})

    chapter_id: Mapped[int] = mapped_column(Integer, ForeignKey("uai_edu_course_chapter.id"), nullable=False, comment="章节ID")
    lesson_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="课时名称")
    lesson_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="课时类型")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
    lecturer: Mapped[int | None] = mapped_column(Integer, comment="授课教师")
    instructor: Mapped[int | None] = mapped_column(Integer, comment="指导教师")
    lesson_resource: Mapped[str | None] = mapped_column(String(200), comment="授课资源")
    lesson_courseware: Mapped[str | None] = mapped_column(String(200), comment="课件资源")
    lesson_tasklist: Mapped[str | None] = mapped_column(String(200), comment="学习任务")
    lesson_exercise: Mapped[str | None] = mapped_column(String(200), comment="课后练习")
    total_duration: Mapped[float | None] = mapped_column(DECIMAL(20, 6), comment="课时时长")
    lesson_desc: Mapped[str | None] = mapped_column(Text, comment="课时描述")


class UaiEduCourseLessonProgress(BaseModel):
    __tablename__ = "uai_edu_course_lesson_progress"
    __table_args__ = ({'comment': '课时学习进度表'})

    course_id: Mapped[int] = mapped_column(Integer, ForeignKey("uai_edu_course.id"), nullable=False, comment="课程ID")
    chapter_id: Mapped[int] = mapped_column(Integer, ForeignKey("uai_edu_course_chapter.id"), nullable=False, comment="章节ID")
    lesson_id: Mapped[int] = mapped_column(Integer, ForeignKey("uai_edu_course_chapter_lesson.id"), nullable=False, comment="课时ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    current_duration: Mapped[float | None] = mapped_column(DECIMAL(20, 6), comment="学习时长")
    study_status: Mapped[int | None] = mapped_column(Integer, comment="学习状态")
