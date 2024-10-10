
# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt
import re

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`

Base = automap_base()

# Use the Base class to reflect the database tables

Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create a session

session = Session(engine)

#################################################
# Flask Setup
#################################################


app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# 1./

# - Start at the homepage.

# - List all the available routes.
@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    )

#2./api/v1.0/precipitation

# - Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.

# - Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)

    12_mnths= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    prev_date = dt.date(12_mnths.year, 12_mnths.month, 12_mnths.day)

    rslts= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_date).order_by(Measurement.date.desc()).all()


    p_dict = dict(rslts)

    print(f"Results for Precipitation - {p_dict}")
    print("Out of Precipitation section.")
    return jsonify(p_dict)

#3./api/v1.0/stations

# - Return a JSON list of stations from the dataset.

#4./api/v1.0/tobs

# - Query the dates and temperature observations of the most-active station for the previous year of data.

# - Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    queryresult = session.query(*sel).all()
    session.close()

    sttns = []
    for station,name,lat,lon,el in queryresult:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)
#5./api/v1.0/<start> and /api/v1.0/<start>/<end>

# - Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

# - For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

# - For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

def get_temps_start(start):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        tmp_dic = {}
        tmp_dic['Minimum Temperature'] = min_temp
        tmp_dic['Average Temperature'] = avg_temp
        tmp_dic['Maximum Temperature'] = max_temp
        temps.append(tmp_dic)

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def get_temps_start_end(start, end):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
              filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in results:
        tmp_dic = {}
        tmp_dic['Minimum Temperature'] = min_temp
        tmp_dic['Average Temperature'] = avg_temp
        tmp_dic['Maximum Temperature'] = max_temp
        temps.append(tmp_dic)

    return jsonify(temps)