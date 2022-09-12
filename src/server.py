#!/usr/bin/env python3
import json
from flask import Flask, json, request
from sqlalchemy import create_engine, cast, Date, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
import models.input_model as input_model
import models.output_model as output_model

app = Flask(__name__)

Session = scoped_session(sessionmaker())


def init():
    engine = create_engine('sqlite:///agdata.db', echo=False)
    Session.configure(bind=engine)


@app.route('/api/weather')
def weather():
    # Get query-string parameters
    # TODO: error check against invalid querystring parameters. Not likely to be a security risk except DDoS but still.
    sid = request.args.get('sid')
    date = request.args.get('date')
    page_string = request.args.get('page')
    page_size_string = request.args.get('pagesize')
    with Session() as session:
        query = session.query(input_model.Weather)

        # Apply filtering
        if sid is not None:
            query = query.filter(input_model.Weather.station_name == sid)
        if date is not None:
            query = query.filter(input_model.Weather.weather_date == date)
        if page_string is not None:
            page = int(page_string)
            if page_size_string is not None:
                page_size = int(page_size_string)
            else:
                page_size = 25
            query = query.slice(page*page_size, (page*page_size)+page_size)

        # Run query
        results = [{
            'Station ID': x.station_name,
            'Date': x.weather_date.strftime('%Y %m %d'),
            'Max Temp (C)': x.max_temp_c}
            for x in list(query)]
        return json.dumps(results)


@app.route('/api/yield')
def corn_yield():
    year = request.args.get('year')
    with Session() as session:
        query = session.query(input_model.CornYield)
        if year is not None:
            query = query.filter(input_model.CornYield.year == year)

        results = [{
            'Year': x.year,
            'Corn Yield': x.corn_yield}
            for x in list(query)]
        return json.dumps(results)


@app.route('/api/weather/stats')
def stats():
    sid = request.args.get('sid')
    year = request.args.get('year')
    page_string = request.args.get('page')
    page_size_string = request.args.get('pagesize')

    with Session() as session:
        query = session.query(output_model.Summary)

        if sid is not None:
            query = query.filter(output_model.Summary.station_name == sid)
        if year is not None:
            query = query.filter(output_model.Summary.year == year)
        if page_string is not None:
            page = int(page_string)
            if page_size_string is not None:
                page_size = int(page_size_string)
            else:
                page_size = 25
            query = query.slice(page*page_size, (page*page_size)+page_size)

        results = [{
            'Station Name': x.station_name,
            'Year': x.year,
            'Avg Max Temp (C)': x.avg_max_temp_c,
            'Avg Min Temp (C)': x.avg_min_temp_c,
            'Total Precipitation': x.total_precipitation}
            for x in list(query)]
        return json.dumps(results)


if __name__ == "__main__":
    init()
    app.run()   

