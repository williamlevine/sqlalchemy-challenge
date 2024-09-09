# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt
from pprint import pprint
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a JSON list of precipitation data from the last 12 months."""
    
    # Convert the query results from precipitation analysis to a dictionary using date as the key and prcp as the value
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()

    precip_dict = {date: prcp for date, prcp in precipitation_data}

    # Return the JSON representation of the dictionary
    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of active stations."""
    
    # Perform a query which finds a list of stations; convert to dictionary
    stations_list = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    stations_dict = {
        station: {
            "name": name, 
            "latitude": latitude, 
            "longitude": longitude, 
            "elevation": elevation
        }
        for station, name, latitude, longitude, elevation in stations_list
    }
    
    # Return the JSON representation of the dictionary
    return jsonify(stations_dict)

    
@app.route("/api/v1.0/tobs")
def temperatures():
    """Return a JSON list of temperature observations from the previous year."""

    # Query for the observed temperatures over the last year at the most active station
    temperature_last_year = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').\
    all()

    # Convert to a dictionary and jsonify
    temps_dict = {date: tobs for date, tobs in temperature_last_year}
    return jsonify(temps_dict)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """Return a JSON list of TMIN, TAVG, TMAX for a specified start or start-end range."""
    
    # Build base query for temperature statistics
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # If an end date is provided, query for the date range between start and end
    if end:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    # Otherwise, query for all dates greater than or equal to the start date
    else:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    
    # Put the results into a dictionary
    temp_stats = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    
    return jsonify(temp_stats)

# Close the session
session.close()

if __name__ == '__main__':
    app.run(debug=True)