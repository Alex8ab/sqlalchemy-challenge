# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Import Flask and jsonify to create a local server and convert the responses to Json representation 
from flask import Flask, jsonify

# Import sqlalchemy to made queries and the engine to conect to DB
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Setup sqlite DB
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask setup
app = Flask(__name__)

# Routes
@app.route("/")
def home():
    return f"""
        <p>Available routes:</p>

        <p><strong>Precipitation (Date and Precipitation):</strong></p>
        <p>/api/v1.0/precipitation</p>

        <p><strong>List of stations:</strong></p>
        <p>/api/v1.0/stations</p>

        <p><strong>Dates and temperature observations of the most active station for the last year:</strong></p>
        <p>/api/v1.0/tobs</p>
  
        <p><strong>List of the minimum temperature, the average temperature, and the max temperature for a given start date (star date has "yyyy-mm-dd" format):</strong></p>
        <p>/api/v1.0/start</p>

        <p><strong>List of the minimum temperature, the average temperature, and the max temperature for dates between the start and end date inclusive (star and end date have "yyyy-mm-dd" format):</strong></p>
        <p>/api/v1.0/start/end</p>
    """


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    # Return the JSON representation of your dictionary.
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary with date as key and precipitation as value
    precipitation = []
    for date, prcp in results:
        precipitation.append({
            date : prcp
        })

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Return a JSON list of stations from the dataset.
    # measures = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    measures = [Station.station]
    session = Session(engine)
    results = session.query(*measures).all()
    session.close()
    
    results = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query the dates and temperature observations of the most active station for the last year of data.
    # Return a JSON list of temperature observations (TOBS) for the previous year.
    last_year_day = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    session = Session(engine)

    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()[0][0]

    results = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date >= last_year_day).\
            filter(Measurement.station == most_active_station).\
            group_by(Measurement.date).all()

    session.close()

    results = list(np.ravel(results))

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start_day(start):
    # List of the minimum temperature, the average temperature, and the max temperature for a given start.
    # When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    results = list(np.ravel(results))
    
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # List of the minimum temperature, the average temperature, and the max temperature for a given start-end.
    # When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    session.close()

    results= list(np.ravel(results))

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)