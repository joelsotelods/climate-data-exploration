

import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, render_template



engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/api/v1.0/precipitation")
def precipitation():
    prcp = session.query(Measurement.date, Measurement.prcp).all()
    all_prcp = []
    for result in prcp:
        row = {}
        row["date"] = prcp[0]
        row["prcp"] = prcp[1]
        all_prcp.append(row)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    station_results = session.query(Station.station, Station.station.name).all()
    station_list = list(np.ravel(station_results))
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()
    temperature_all = []
    for result in tobs:
        row = {}
        row["date"] = tobs[0]
        row["tobs"] = tobs[1]
        temperature_all.append(row)

    return jsonify(temperature_all)


@app.route("/api/v1.0/<start>")
def start_temp(start):
    startdate=start
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    print(results)
    for row in session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= startdate).all():
        print(row)
    
    data_list = []
    for result in results:
        row = {}
        row['startdate'] = startdate
        row['avg'] = float(result[0])
        row['max'] = float(result[1])
        row['min'] = float(result[2])
        data_list.append(row)

    return jsonify(data_list)

@app.route("/api/v1.0/<start>/<end>")
def between_temp(start, end):
    start_date=start
    end_date= end
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    print(results)

    data_list = []
    for result in results:
        row = {}
        row['startdate'] = start_date
        row['end_date'] = end_date
        row['avg'] = float(result[0])
        row['max'] = float(result[1])
        row['min'] = float(result[2])
        data_list.append(row)

    return jsonify(data_list)


if __name__ == '__main__':
    app.run(debug=True)