#!/usr/bin/env python
# coding: utf-8

# Routes
# /
# Home page.
# 
# List all routes that are available.
# 
# 
# /api/v1.0/precipitation
# 
# Convert the query results to a dictionary using date as the key and prcp as the value.
# 
# Return the JSON representation of your dictionary.
# 
# 
# 
# /api/v1.0/stations
# 
# Return a JSON list of stations from the dataset.
# 
# 
# 
# 
# /api/v1.0/tobs
# 
# 
# Query the dates and temperature observations of the most active station for the last year of data.
# 
# Return a JSON list of temperature observations (TOBS) for the previous year.
# 
# 
# 
# 
# /api/v1.0/<start> and /api/v1.0/<start>/<end>
# 
# 
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# 
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# 
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
# 

# In[1]:


# Import the dependencies
import numpy as np
import pandas as pd

import datetime as dt
from dateutil.relativedelta import relativedelta

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, MetaData, Table, Column, ForeignKey, inspect, func

from flask import Flask, jsonify


# In[2]:


engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# In[3]:


# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)


# In[4]:


# View all of the classes that automap found
Base.classes.keys()


# In[5]:


# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# In[6]:


# Inspecting the column name and type for 'measurement'
#inspector = inspect(engine)
#inspector.get_table_names()
#columns = inspector.get_columns('measurement')
#for column in columns:
    #print(column["name"], column["type"])


# In[7]:


# Inspecting the column name and type for 'station'
#inspector = inspect(engine)
#inspector.get_table_names()
#columns = inspector.get_columns('station')
#for column in columns:
    #print(column["name"], column["type"])


# In[8]:


# Flask Setup
app = Flask(__name__)


# In[9]:


# Flask route "homepage"
@app.route("/")

def Home():

    """

        List all the available routes in the app.

    """

    return (

        f"Welcome to the Hawaii Weather Home page!<br/>"

        f"Available Routes:<br/>"

        f"/api/v1.0/precipitation<br/>"

        f"/api/v1.0/stations<br/>"

        f"/api/v1.0/tobs<br/><br/>"

        f"Please enter start date in below api in the format YYYY-MM-DD<br/>"

        f"/api/v1.0/<start_date><br/><br/>"

        f"Please enter start and end dates in below api in the format YYYY-MM-DD/YYYY-MM-DD<br/>"

        f"/api/v1.0/<start_date>/<end_date><br/>"

    )


# In[10]:


# Flask route "precipitation"
@app.route("/api/v1.0/precipitation")

def precipitation():

# Create our session (link) from Python to the DB
    session = Session(engine)

#  Calculate the "max date" in the Measurement Table
    max_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

# Calculate the date a year before
# (the date to be used to get all the records greater than the date)
    previous_year_date = (dt.datetime.strptime(max_date[0], '%Y-%m-%d').date() - relativedelta(years=1)).isoformat()

#  Perform a query to retrieve the date and precipitation data
    measurement_result = session.query(Measurement.date, Measurement.prcp).    filter(Measurement.date >= previous_year_date).    order_by( Measurement.date.desc(), Measurement.station.desc()).all()

# Close the session after the query
    session.close()
    
# Create a dictionary from the row data and append to a list of prcp_list   
    prcp_list = []
    for date, prcp in measurement_result:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_list.append(prcp_dict)

# Returns the precipitation for past one year from the max date in the dataset
    return jsonify(prcp_list)


# In[11]:


# Flask route "stations"
@app.route("/api/v1.0/stations")

def stations():

# Create our session (link) from Python to the DB
    session = Session(engine)

#  Perform a query to retrieve the list of stations ordered by Station
    station_result = session.query(Measurement.station, Station.name).    filter(Measurement.station == Station.station).    group_by(Measurement.station).    order_by(Measurement.station.asc()).all()

# Close the session after the query
    session.close()
        
# Create a dictionary from the row data and append to a list of station_list    
    station_list = []
    for station, station_name in station_result:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Station Name"] = station_name
        station_list.append(station_dict)

# Returns a list of distinct weather stations (Id and the Name) from the measurement table
    return jsonify(station_list)


# In[12]:


# Flask route "tobs"
@app.route("/api/v1.0/tobs")

def tobs():

# Create our session (link) from Python to the DB
    session = Session(engine)

# Calculate the "max date" in the Measurement Table
    max_date = session.query(Measurement.date).    order_by(Measurement.date.desc()).first()
    
# Calculate the date a year before i.e.the date to be used to get all the records greater than the date
    previous_year_date = (dt.datetime.strptime(max_date[0], '%Y-%m-%d').date() - relativedelta(years=1)).isoformat()
    
# Get the most active station (Station with most tobs records is most active)
    most_active_result = session.query(Measurement.station, func.count(Measurement.station)).    group_by(Measurement.station).    order_by(func.count(Measurement.station).desc()).first()
    
# Get the tobs for the dates for the station identified above
    tobs_result = session.query(Measurement.station,Measurement.date,Measurement.tobs).    filter(Measurement.station == most_active_result[0]).    filter(Measurement.date >= previous_year_date).    order_by(Measurement.station.asc(),Measurement.date.asc()).all()
    
# Close the session after the query
    session.close()
    
         
# Create a dictionary from the row data and append to a list of tobs_list    
    tobs_list = []
    for station, date, tobs in tobs_result:
        tobs_dict = {}
        tobs_dict["Station"] = station
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_list.append(tobs_dict)

# Return the Temperatures for the most active station for a year
    return jsonify(tobs_list)

# Date validation function
def validate_date(date_text):
    try:
        if date_text != dt.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False


# In[13]:


# Flask route "start_date"
@app.route("/api/v1.0/<start_date>")

def start(start_date):

# Validate the start date, raise error for invalid date entry.
    if not validate_date(start_date):
        return jsonify({"error": f"Please, specify the date in 'YYYY-MM-DD' format: The entered date '{start_date}' is not valid."}), 404
    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')

# Create our session (link) from Python to the DB
    session = Session(engine)
    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    avg_temp = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date >= start_date).scalar()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()

# Close the session after the query
    session.close()

# Return the Minimum, Average and Maximum temperatures for the dates greater then the user entered date
    result = [{"Minimum Temp":min_temp}, {"Average Temp":avg_temp}, {"Maximum Temp":max_temp}]
    return jsonify(result)


# In[14]:


# Flask route "start_date, end_date"
@app.route("/api/v1.0/<start_date>/<end_date>")

def start_end(start_date, end_date):

# Validate the start and end dates and also check that the end date is greater than start date, raise error for invalid date entry.
    if not validate_date(start_date):
        return jsonify({"error": f"Please, specify the start date in 'YYYY-MM-DD' format: The entered date '{start_date}' is not valid."}), 404
    if not validate_date(end_date):
        return jsonify({"error": f"Please, specify the end date in 'YYYY-MM-DD' format: The entered date '{end_date}' is not valid."}), 404
    if end_date < start_date:
        return jsonify({"error": f"Please, specify start date less then end date. The dates entered are '{start_date}' and '{end_date}'"}), 404

    start_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

# Create our session (link) from Python to the DB
    session = Session(engine)

    min_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()
    avg_temp = session.query(func.round(func.avg(Measurement.tobs))).filter(Measurement.date.between(start_date, end_date)).scalar()
    max_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).scalar()


# Close the session after the query
    session.close()

# Return the Minimum, Average and Maximum temperatures for the specified date range.
    result = [{"Minimum Temp":min_temp}, {"Average Temp":avg_temp}, {"Maximum Temp":max_temp}]
    return jsonify(result)


# In[15]:


if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




