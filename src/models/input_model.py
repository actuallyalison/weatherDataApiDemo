from sqlalchemy import Table, Column, Integer, String, Date, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Weather(Base):
    __tablename__ = "weather_data"

    station_name = Column(String, primary_key=True)
    weather_date = Column(Date, primary_key=True)

    max_temp_c = Column(Integer)
    min_temp_c = Column(Integer)
    precipitation = Column(Integer)


class CornYield(Base):
    __tablename__ = "US_corn_grain_yield"

    year = Column(Integer, primary_key=True)
    corn_yield = Column(Integer)





