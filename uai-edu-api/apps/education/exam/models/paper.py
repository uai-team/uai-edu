from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduExamPaper(BaseModel):
    __tablename__ = "uai_edu_exam_paper"
    __table_args__ = ({'comment': '考试试卷表'})

    category_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_category.id"), nullable=False, comment="学科科目")
    dept_id: Mapped[int] = mapped_column(ForeignKey("vadmin_auth_dept.id"), comment="可见范围")
    paper_name: Mapped[str] = mapped_column(String(500), nullable=False, comment="试卷名称")
    paper_time: Mapped[int] = mapped_column(Integer, comment="考试时长")
    paper_score: Mapped[int] = mapped_column(Integer, comment="试卷总分")
