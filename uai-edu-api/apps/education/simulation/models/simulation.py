from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.education.category.models import UaiEduCategory
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text
from .m2m import uai_edu_simulation_categories


class UaiEduSimulation(BaseModel):
    __tablename__ = "uai_edu_simulation"
    __table_args__ = ({'comment': '仿真信息表'})

    simulation_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="仿真名称")
    simulation_cover: Mapped[str] = mapped_column(String(200), nullable=False, comment="仿真封面")
    simulation_path: Mapped[str | None] = mapped_column(String(200), comment="仿真资源")
    simulation_desc: Mapped[str | None] = mapped_column(Text, comment="仿真描述")
    simulation_prompt: Mapped[str | None] = mapped_column(Text, comment="系统提示词")

    categories: Mapped[set[UaiEduCategory]] = relationship(secondary=uai_edu_simulation_categories)
