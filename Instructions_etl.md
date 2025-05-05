# Weather ETL Project

## Overview
This project processes historical weather data from text files and performs:
- ETL (Extract, Transform, Load) to store clean data in a relational database
- Yearly statistical analysis per station

## Components

### 1. `models.py`
Defines two SQLAlchemy ORM models:
- `WeatherData`: stores raw daily weather records
- `WeatherSummary`: stores calculated yearly summaries

### 2. `ingestion.py`
Parses `.txt` weather files and inserts them into the `weather_data` table, skipping duplicates and handling missing data.

### 3. `analysis.py`
Performs analysis:
- Average max and min temperatures
- Total precipitation
Then saves the results in the `weather_summary` table.

### 4. `main.py`
Coordinates the whole ETL process:
1. Runs ingestion
2. Runs analysis

## How to Run

1. Place `USC00110072.txt` in the project folder.
2. Install SQLAlchemy:
   ```bash
   pip install sqlalchemy
   ```
3. Run the project:
   ```bash
   python main.py
   ```

## Output
- Logs: `ingestion.log`, `analysis.log`
- SQLite DB: `weather.db`
