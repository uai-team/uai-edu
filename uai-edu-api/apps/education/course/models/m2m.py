from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


uai_edu_course_zones = Table(
    "uai_edu_course_zones",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("uai_edu_course.id", ondelete="CASCADE")),
    Column("zone_id", Integer, ForeignKey("uai_edu_zone.id", ondelete="CASCADE")),
)

uai_edu_course_categories = Table(
    "uai_edu_course_categories",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("uai_edu_course.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("uai_edu_category.id", ondelete="CASCADE")),
)
