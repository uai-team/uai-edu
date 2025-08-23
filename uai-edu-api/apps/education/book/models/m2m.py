from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


uai_edu_book_categories = Table(
    "uai_edu_book_categories",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("uai_edu_book.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("uai_edu_category.id", ondelete="CASCADE")),
)
