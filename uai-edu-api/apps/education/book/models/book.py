from sqlalchemy.orm import relationship, Mapped, mapped_column
from apps.education.category.models import UaiEduCategory
from db.db_base import BaseModel
from sqlalchemy import String, ForeignKey, Integer, Text
from .m2m import uai_edu_book_categories


class UaiEduBook(BaseModel):
    __tablename__ = "uai_edu_book"
    __table_args__ = ({'comment': '教材信息表'})

    book_name: Mapped[str] = mapped_column(String(200), nullable=False, comment="教材名称")
    book_cover: Mapped[str] = mapped_column(String(200), nullable=False, comment="教材封面")
    book_path: Mapped[str | None] = mapped_column(String(200), comment="教材资源")
    book_desc: Mapped[str | None] = mapped_column(Text, comment="教材描述")

    categories: Mapped[set[UaiEduCategory]] = relationship(secondary=uai_edu_book_categories)
