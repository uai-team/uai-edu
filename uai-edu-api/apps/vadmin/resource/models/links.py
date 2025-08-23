from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer


class VadminLinks(BaseModel):
    __tablename__ = "vadmin_resource_links"
    __table_args__ = ({'comment': '链接素材表'})

    link_type: Mapped[str] = mapped_column(String(10), nullable=False, comment="链接类型")
    image_url: Mapped[str] = mapped_column(String(500), nullable=True, comment="图片链接")
    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="链接名称")
    url: Mapped[str] = mapped_column(String(500), nullable=False, comment="链接地址")
    target: Mapped[str] = mapped_column(String(10), nullable=False, comment="打开目标")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
