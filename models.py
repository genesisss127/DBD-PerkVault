
from sqlalchemy import Column, Integer, String, Text

from database import Base


class Perk(Base):
    __tablename__ = "perks"

    id = Column("rowid", Integer, primary_key=True)
    icon = Column("Column1", String, nullable=True)
    name = Column("Column2", String, nullable=False)
    description = Column("Column3", Text, nullable=False)
    character = Column("Column4", String, nullable=False)
