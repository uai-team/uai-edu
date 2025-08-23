from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduQuestion(BaseModel):
    __tablename__ = "uai_edu_question"
    __table_args__ = ({'comment': '题目表'})

    question_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="题目类型")
    category_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_category.id"), nullable=False, comment="学科科目")
    lesson_id: Mapped[int | None] = mapped_column(ForeignKey("uai_edu_course_chapter_lesson.id"), comment="知识点")
    question_title: Mapped[str] = mapped_column(String(500), nullable=False, comment="题目内容")
    difficult: Mapped[int | None] = mapped_column(Integer, comment="题目难度")
    question_items: Mapped[str | None] = mapped_column(Text, comment="答案选项")
    correct: Mapped[str | None] = mapped_column(Text, comment="正确答案")
    analyze: Mapped[str | None] = mapped_column(Text, comment="答案解析")
