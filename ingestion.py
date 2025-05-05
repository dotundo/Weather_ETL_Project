import logging
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base, WeatherData

logging.basicConfig(filename='ingestion.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def parse_and_ingest(file_path, station_id):
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 4:
                continue
            date_str, max_t, min_t, prcp = parts
            try:
                date = datetime.strptime(date_str, "%Y%m%d").date()
                max_t = None if int(max_t) == -9999 else int(max_t) / 10.0
                min_t = None if int(min_t) == -9999 else int(min_t) / 10.0
                prcp = None if int(prcp) == -9999 else int(prcp) / 100.0
                exists = session.query(WeatherData).filter_by(station_id=station_id, date=date).first()
                if not exists:
                    record = WeatherData(station_id=station_id, date=date, max_temp=max_t,
                                         min_temp=min_t, precipitation=prcp)
                    session.add(record)
            except Exception as e:
                logging.error(f"Failed to parse line: {line.strip()} - {e}")
    session.commit()
    logging.info("Ingestion complete.")
