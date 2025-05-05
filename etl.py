import logging
from sqlalchemy import create_engine
from models import Base
from ingestion import parse_and_ingest
from analysis import compute_weather_summary

logging.basicConfig(filename='etl.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

engine = create_engine('sqlite:///weather.db')
Base.metadata.create_all(engine)

def run_etl(file_path, station_id):
    logging.info("Starting ETL process...")
    parse_and_ingest(file_path, station_id)
    compute_weather_summary()
    logging.info("ETL process completed.")

run_etl("USC00110072.txt", "USC00110072")
