from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduHomework(BaseModel):
    __tablename__ = "uai_edu_homework"
    __table_args__ = ({'comment': '家庭作业表'})

    category_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_category.id"), nullable=False, comment="学科科目")
    dept_id: Mapped[int] = mapped_column(ForeignKey("vadmin_auth_dept.id"), comment="可见范围")
    homework_name: Mapped[str] = mapped_column(String(500), nullable=False, comment="作业名称")
    others: Mapped[str|None] = mapped_column(Text, comment="其他作业")
