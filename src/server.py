#!/usr/bin/env python3
import json
from flask import Flask, json, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import models.input_model as input_model

app = Flask(__name__)

Session = scoped_session(sessionmaker())


def init():
    engine = create_engine('sqlite:///agdata.db', echo=False)
    Session.configure(bind=engine)


@app.route('/api/weather')
def weather():
    sid = request.args.get('sid')
    # TODO: implement date filter (requires decisions: format, year vs full date, range allowed?)
    # TODO: implement pagination (qs param for page number? Qty per page?)
    date = request.args.get('date')
    with Session() as session:
        query = session.query(input_model.Weather)
        if sid is not None:
            query = query.filter(input_model.Weather.station_name == sid)
        results = [{
            'Station ID': x.station_name,
            'Date': x.weather_date.strftime('%Y %m %d'),
            'Max Temp (C)': x.max_temp_c}
            for x in list(query)]
        return json.dumps(results)


@app.route('/api/yield')
def corn_yield():
    year = request.args.get('year')
    # TODO: implement route


@app.route('/api/weather/stats')
def stats():
    sid = request.args.get('sid')
    year = request.args.get('year')
    # TODO: implement route


if __name__ == "__main__":
    init()
    app.run()   

