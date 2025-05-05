import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func
from models import WeatherData, WeatherSummary

logging.basicConfig(filename='analysis.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

engine = create_engine('sqlite:///weather.db')
Session = sessionmaker(bind=engine)
session = Session()

def compute_weather_summary():
    try:
        results = (
            session.query(
                WeatherData.station_id,
                func.strftime('%Y', WeatherData.date).label('year'),
                func.avg(WeatherData.max_temp).label('avg_max_temp'),
                func.avg(WeatherData.min_temp).label('avg_min_temp'),
                func.sum(WeatherData.precipitation).label('total_precipitation')
            )
            .group_by(WeatherData.station_id, func.strftime('%Y', WeatherData.date))
            .all()
        )
        count = 0
        for row in results:
            station_id, year, avg_max, avg_min, total_prcp = row
            if not session.query(WeatherSummary).filter_by(station_id=station_id, year=year).first():
                summary = WeatherSummary(
                    station_id=station_id,
                    year=int(year),
                    avg_max_temp=round(avg_max, 2) if avg_max else None,
                    avg_min_temp=round(avg_min, 2) if avg_min else None,
                    total_precipitation=round(total_prcp, 2) if total_prcp else None
                )
                session.add(summary)
                count += 1
        session.commit()
        logging.info(f"Inserted {count} summary records.")
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
