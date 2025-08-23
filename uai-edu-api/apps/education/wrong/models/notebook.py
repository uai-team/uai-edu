from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, DateTime, Text


class UaiEduUserWrongNotebook(BaseModel):
    __tablename__ = "uai_edu_user_wrong_notebook"
    __table_args__ = ({'comment': '用户错题表'})

    answer_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_exam_user.id"), nullable=False, comment="考试ID")
    question_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_question.id"), nullable=False, comment="题目ID")
    wrong_datetime: Mapped[DateTime] = mapped_column(DateTime, nullable=False, comment='创建时间')
    review_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="复习次数")
    last_review_time: Mapped[DateTime | None] = mapped_column(DateTime, nullable=True, comment='上次复习时间')
    user_answer: Mapped[str | None] = mapped_column(Text, comment="用户答案")
