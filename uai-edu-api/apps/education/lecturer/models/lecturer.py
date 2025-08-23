from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.education.zone.models import UaiEduZone
from apps.education.category.models import UaiEduCategory
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text


class UaiEduLecturer(BaseModel):
    __tablename__ = "uai_edu_lecturer"
    __table_args__ = ({'comment': '教师信息表'})

    lecturer_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="教师名称")
    lecturer_avatar: Mapped[str] = mapped_column(String(200), nullable=False, comment="教师头像")
    lecturer_title: Mapped[str] = mapped_column(String(100), comment="教师职称")
    lecturer_position: Mapped[str] = mapped_column(String(100), comment="教师职务")
    lecturer_desc: Mapped[str | None] = mapped_column(Text, comment="教师描述")
