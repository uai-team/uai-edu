from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduExamPaperTitle(BaseModel):
    __tablename__ = "uai_edu_exam_paper_title"
    __table_args__ = ({'comment': '考试试卷标题表'})

    paper_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_exam_paper.id"), nullable=False, comment="试卷ID")
    title_name: Mapped[str] = mapped_column(String(500), nullable=False, comment="标题名称")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
