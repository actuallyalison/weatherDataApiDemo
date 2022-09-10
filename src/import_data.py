#!/usr/bin/env python3
import os
import datetime
from sqlalchemy import create_engine, MetaData, select
import models.input_model as model
from sqlalchemy.orm import sessionmaker, scoped_session
import time

print('Started at: ',time.strftime('%a, %d %b %Y %H:%M:%S'))

engine = create_engine('sqlite:///agdata.db', echo = False)

# Drop and refill is much more efficient if valid for this use case.
# In addition to adding this line, change merge calls to use add instead:
#model.Base.metadata.drop_all(engine)

# create or update the schema 
model.Base.metadata.create_all(engine)

def check_null_number(value):
    return None if value == -9999 else value

print('Importing weather data...')

total_row_count = 0
with os.scandir('../wx_data') as data_files:
    for file in data_files:
        with open(file, 'r') as f:
            total_wx_data = []
            data = f.readlines()

            # split on tabs, strip whitespace and newlines
            split_data = [
                    [i.strip() for i in x.strip().split('\t')]
                    for x in data]

            # use file name without extension as first column
            station_name = file.name.split('.')[0]
            for i in split_data:

                # inflate object:
                weather_date = datetime.date(
                        int(i[0][:4]),
                        int(i[0][4:6]),
                        int(i[0][6:]))
                max_temp_c = check_null_number(int(i[1]))
                min_temp_c = check_null_number(int(i[2]))
                precipitation = check_null_number(int(i[3]))
                o = model.Weather(
                        station_name=station_name,
                        weather_date=weather_date,
                        max_temp_c=max_temp_c,
                        min_temp_c=min_temp_c,
                        precipitation=precipitation)
                total_wx_data.append(o)
                
            Session = scoped_session(sessionmaker())
            Session.configure(bind=engine)

            with Session() as session:
                for row in total_wx_data:
                    session.merge(row)
                session.commit()
            
            total_row_count += len(total_wx_data)
        
    print(f'Successfully imported {total_row_count} weather data rows.')

print('Importing corn yield data...')

corn_yield_data = []
with open('../yld_data/US_corn_grain_yield.txt', 'r') as f:
    data = f.readlines()
    split_data = [
            [i.strip() for i in x.strip().split('\t')]
            for x in data]
    for i in split_data:
        year = int(i[0])
        corn_yield = int(i[1])
        o = model.CornYield(
                year = year,
                corn_yield = corn_yield)
        corn_yield_data.append(o)

Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
with Session() as session:
    for row in corn_yield_data:
        session.merge(row)
    session.commit()

    total_row_count = len(corn_yield_data)

print(f'Successfully imported {total_row_count} corn yield rows.')

print('Ended at: ',time.strftime('%a, %d %b %Y %H:%M:%S'))


