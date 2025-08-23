from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer


class UaiEduCarousel(BaseModel):
    __tablename__ = "uai_edu_carousel"
    __table_args__ = ({'comment': '轮播图表'})

    carousel_img: Mapped[str] = mapped_column(String(500), nullable=False, comment="图片链接")
    carousel_title: Mapped[str] = mapped_column(String(255), nullable=True, comment="横幅名称")
    carousel_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="链接地址")
    carousel_target: Mapped[str] = mapped_column(String(10), nullable=True, comment="打开目标")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
