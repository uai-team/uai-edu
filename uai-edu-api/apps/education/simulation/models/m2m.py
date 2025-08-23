from db.db_base import Base
from sqlalchemy import ForeignKey, Column, Table, Integer


uai_edu_simulation_categories = Table(
    "uai_edu_simulation_categories",
    Base.metadata,
    Column("simulation_id", Integer, ForeignKey("uai_edu_simulation.id", ondelete="CASCADE")),
    Column("category_id", Integer, ForeignKey("uai_edu_category.id", ondelete="CASCADE")),
)
