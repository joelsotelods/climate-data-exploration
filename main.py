

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template
from datetime import datetime as dt2

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


#### Home API response ####

@app.route("/")
def home():
    return render_template('index.html')


#### Precipitation API response ####

@app.route("/api/v1/prcp")
def prcp():
    
    result = session.query(Measurement.date, Measurement.prcp).all()
    
    #print(result)
    json_row = {}
    
    for row in result:
        json_row[row[0]] = row[1]
        #print(json_row)
 
    return jsonify(json_row)


#### Stations API response ####

@app.route("/api/v1/stations")
def stations():
    result = session.query(Station.station).distinct().all()
    st_list = list(np.ravel(result))
    
    return jsonify(st_list)


#### Temperature Observations API response ####

@app.route("/api/v1/tobs")
def tobs():

    for row in session.\
                query(Measurement.date).\
                order_by(Measurement.date.desc()).\
                limit(1):
        lastdate = row[0]
                
    print(lastdate)

    finaldate = dt2.strptime(lastdate,'%Y-%m-%d')

    print(finaldate)

    new_day = finaldate.day
    new_month = finaldate.month
    new_year = finaldate.year-1
    ## se me olvidó el caso de los años bisiesto (sorry)

    if new_day>9 and new_month>9:
        initdate = (f'{new_year}-{new_month}-{new_day}')
    elif new_day<9 and new_month>9:
        initdate = (f'{new_year}-{new_month}-0{new_day}')
    elif new_day>9 and new_month<9:
        initdate = (f'{new_year}-0{new_month}-{new_day}')
    else:
        initdate = (f'{new_year}-0{new_month}-0{new_day}')

    print(initdate)

    result = session.query(Measurement.date, Measurement.tobs).\
                filter((Measurement.date >= initdate) & (Measurement.date <= lastdate)).\
                all()

    tobs_all = []

    for row in result:
        tobs_all.append(row[1])


    return jsonify(tobs_all)


#### Temperature by start date API response ####

@app.route("/api/v1/<start_date>")
def start_temp(start_date):
    result = session.\
                query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
                filter(Measurement.date >= start_date).\
                all()
    print(result)

    json_row = {}
    json_row['start_date'] = start_date
    json_row['tavg'] = result[0][0]
    json_row['tmax'] = result[0][1]
    json_row['tmin'] = result[0][2]

    return jsonify(json_row)


#### Temperature by Range of dates API response ####

@app.route("/api/v1/<start_date>/<end_date>")
def between_temp(start_date, end_date):
    result = session.\
                query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
                filter( (Measurement.date >= start_date) & (Measurement.date <= end_date) ).\
                all()
    print(result)

    json_row = {}
    json_row['start_date'] = start_date
    json_row['end_date'] = end_date
    json_row['tavg'] = result[0][0]
    json_row['tmax'] = result[0][1]
    json_row['tmin'] = result[0][2]

    return jsonify(json_row)


if __name__ == '__main__':
    app.run(debug=True)