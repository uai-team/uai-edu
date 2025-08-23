from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduExamPaperTitleQuestions(BaseModel):
    __tablename__ = "uai_edu_exam_paper_title_questions"
    __table_args__ = ({'comment': '考试试卷题目表'})

    title_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_exam_paper_title.id"), nullable=False, comment="标题ID")
    question_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_question.id"), nullable=False, comment="题目ID")
    score: Mapped[int | None] = mapped_column(Integer, comment="分数")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
