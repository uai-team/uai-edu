from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer


class UaiEduCategory(BaseModel):
    __tablename__ = "uai_edu_category"
    __table_args__ = ({'comment': '类目表'})

    category_type: Mapped[str] = mapped_column(String(20), nullable=False, comment="类目类型")
    category_name: Mapped[str] = mapped_column(String(100), nullable=False, comment="类目名称")
    order: Mapped[int | None] = mapped_column(Integer, comment="显示排序")
    desc: Mapped[str | None] = mapped_column(String(255), comment="描述")

    parent_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("uai_edu_category.id", ondelete='CASCADE'),
        comment="上级类目"
    )
