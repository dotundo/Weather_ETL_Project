from sqlalchemy import Column, Integer, Float, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    max_temp = Column(Float)
    min_temp = Column(Float)
    precipitation = Column(Float)
    __table_args__ = (UniqueConstraint('station_id', 'date', name='_station_date_uc'),)

class WeatherSummary(Base):
    __tablename__ = 'weather_summary'
    id = Column(Integer, primary_key=True)
    station_id = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    avg_max_temp = Column(Float)
    avg_min_temp = Column(Float)
    total_precipitation = Column(Float)
    __table_args__ = (UniqueConstraint('station_id', 'year', name='_station_year_uc'),)
