import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# import flask

from flask import Flask
from flask import jsonify
# create app

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect database into new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# save references to table
Measurement = Base.classes.measurement
Station = Base.classes.station

# flast setup
app = Flask(__name__)

# flask routes

@app.route('/')
def home():
    """List all available api routes."""
    return (
        f"Available Routes :<br/>"
        f"/api/v1.0/precipitation</br>"
        f"/api/v1.0/stations</br>"
        f"/api/v1.0/tobs</br>"
        f"/api/v1.0/temp</br>"
        )


@app.route('/api/v1.0/precipitation')
def precipitation():
    # create session from python to db
    session = Session(engine)
    # query precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Convert the query results to a dictionary using `date` as the key and `prcp` as the value, and add to list.

    precip_data = []
    for date, precipitation in results:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = precipitation
        precip_data.append(precip_dict)

    # Return the JSON representation of dictionary.
    return jsonify(precip_data)


@app.route('/api/v1.0/stations')
def stations():
    # create session from python to db
    session = Session(engine)
    # query station names
    results = session.query(Station.name).all()
    session.close()
    # convert tuple into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    # create session from python to db
    session = Session(engine)
    # query measurement dates and temps for a year from station USC00519281
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.date <= '2017-08-23').\
    filter(Measurement.station == "USC00519281").all()
    session.close()
    # convert query results into a dictionary with date as the key and temp as value, and add to list
    temp_data = []
    for date, temperature in results:
        temp_dict = {}
        temp_dict['date'] = date
        temp_dict['temperature'] = temperature
        temp_data.append(temp_dict)
    
    # Return the JSON representation of dictionary.
    return jsonify(temp_data)

@app.route('/api/v1.0/temp/<start>')
# create decorator with no end date
def temp(start=None):
    # create session from python to db
    session = Session(engine)
    # query results
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs).\
       filter(Measurement.date >= start)).all()
       
    # Return the JSON representation of dictionary.
    return jsonify(results)

@app.route('/api/v1.0/temp/<start>/<end>')
# create second decorator with start and end date
def temp_end(start=None,end=None):
    # create session from python to db
    session = Session(engine)
    # query results
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs).\
       filter(Measurement.date >= start).filter(Measurement.date <= end)).all()
    # return json representation of dictonary
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)