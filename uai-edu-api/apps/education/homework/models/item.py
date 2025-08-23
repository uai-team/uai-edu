from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduHomeworkItem(BaseModel):
    __tablename__ = "uai_edu_homework_item"
    __table_args__ = ({'comment': '家庭作业详情表'})

    homework_id: Mapped[int] = mapped_column(ForeignKey("uai_edu_homework.id"), nullable=False, comment="作业ID")
    item_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="作业项类型")
    resource_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="资源ID")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
