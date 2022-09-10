#!/usr/bin/env python3
from sqlalchemy import create_engine, extract, func
from sqlalchemy.orm import sessionmaker, scoped_session

import models.input_model as input_model
import models.output_model as output_model

engine = create_engine('sqlite:///agdata.db', echo=False)

# create or update the output model's schema 
output_model.Base.metadata.create_all(engine)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)

with Session() as session:

    max_temp_results = session.query(
                input_model.Weather.station_name.label('name'),
                extract('year', input_model.Weather.weather_date).label('year'),
                ((func.sum(input_model.Weather.max_temp_c) / func.count(input_model.Weather.max_temp_c)) / 10
                 ).label('value')  # average, convert from tenths of degree
            ).filter(
                input_model.Weather.max_temp_c is not None
            ).group_by(
                input_model.Weather.station_name,
                extract('year', input_model.Weather.weather_date)
            ).order_by(
                extract('year', input_model.Weather.weather_date)
            )

    min_temp_results = session.query(
                input_model.Weather.station_name.label('name'),
                extract('year', input_model.Weather.weather_date).label('year'),
                ((func.sum(input_model.Weather.min_temp_c) / func.count(input_model.Weather.min_temp_c)) / 10
                 ).label('value')  # average, convert from tenths of degree
            ).filter(
                input_model.Weather.min_temp_c is not None
            ).group_by(
                input_model.Weather.station_name,
                extract('year', input_model.Weather.weather_date)
            )

    precipitation_results = session.query(
                input_model.Weather.station_name.label('name'),
                extract('year', input_model.Weather.weather_date).label('year'),
                (func.sum(input_model.Weather.precipitation) / 100)
                .label('value')  # sum, convert from tenths of mm to cm
            ).filter(
                input_model.Weather.precipitation is not None
            ).group_by(
                input_model.Weather.station_name,
                extract('year', input_model.Weather.weather_date)
            )

    combined_results = {} 

    for result in max_temp_results:
        key = (result.name, result.year)
        if result.value is not None:
            combined_results[key] = [result.value, None, None]

    for result in min_temp_results:
        key = (result.name, result.year)
        if result.value is not None:
            if key in combined_results:
                combined_results[key] = [combined_results[key][0], result.value, None]
            else:
                combined_results[key] = [None, result.value, None]

    for result in precipitation_results:
        key = (result.name, result.year)
        if result.value is not None:
            if key in combined_results:
                combined_results[key] = [combined_results[key][0], combined_results[key][1], result.value]
            else:
                combined_results[key] = [None, None, result.value]

    output_results_list = [list(key)+combined_results[key] for key in combined_results]
    output_results = [output_model.Summary(
        station_name=row[0],
        year=row[1],
        avg_max_temp_c=row[2],
        avg_min_temp_c=row[3],
        total_precipitation=row[4]
    ) for row in output_results_list]

    for row in output_results:
        session.merge(row)

    session.commit()




