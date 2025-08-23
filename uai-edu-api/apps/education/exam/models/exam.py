from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduExamUser(BaseModel):
    __tablename__ = "uai_edu_exam_user"
    __table_args__ = ({'comment': '用户考试表'})

    paper_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_exam_paper.id"), nullable=False, comment="试卷ID")
    user_id: Mapped[int] = mapped_column(ForeignKey("vadmin_auth_user.id"), comment="用户ID")
    score: Mapped[int | None] = mapped_column(Integer, comment="分数")
    

class UaiEduExamUserAnswer(BaseModel):
    __tablename__ = "uai_edu_exam_user_answer"
    __table_args__ = ({'comment': '用户考试答案表'})

    answer_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_exam_user.id"), nullable=False, comment="考试ID")
    question_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_question.id"), nullable=False, comment="题目ID")
    correct: Mapped[bool] = mapped_column(Integer, comment="是否正确")
    score: Mapped[int | None] = mapped_column(Integer, comment="分数")
    user_answer: Mapped[str | None] = mapped_column(Text, comment="用户答案")
