from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import Base, BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
# from apps.education.course.models.m2m import uai_edu_course_zones, uai_edu_course_categories


class UaiEduZone(BaseModel):
    __tablename__ = "uai_edu_zone"
    __table_args__ = ({'comment': '专区表'})

    zone_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="专区类型")
    zone_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="专区名称")
    zone_desc: Mapped[str | None] = mapped_column(String(255), comment="专区描述")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
    courses = relationship("UaiEduCourse", secondary="uai_edu_course_zones", back_populates="zones")
    # courses: Mapped[set[UaiEduCourse]] = relationship(secondary=uai_edu_course_zones)