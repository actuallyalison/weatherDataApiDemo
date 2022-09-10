from sqlalchemy import Table, Column, Integer, String, Date, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Summary(Base):
    __tablename__ = "summary"

    station_name = Column(String, primary_key=True)
    year = Column(Integer, primary_key=True)
    avg_max_temp_c = Column(Integer)
    avg_min_temp_c = Column(Integer)
    total_precipitation = Column(Integer)



