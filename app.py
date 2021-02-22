#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
import datetime as dt
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement =  Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
# Homepage
@app.route("/")
def homepage():
     return (
         f"Welcome to the Climate API!<br/>"
         f"Available Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"/api/v1.0/stations<br/>"
         f"/api/v1.0/tobs<br/>"
         f"/api/v1.0/<start><br/>"
         f"/api/v1.0/<start><end><br/>"
    )
########

# Precipitation Page
# Return a list of Date and Precipitation. 
# Convert each sub-list to dictionaries. 
@app.route("/api/v1.0/precipitation/")
def Measurement_dict():

###########################################################
## QUERY ##
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    Measurement_qry = session.query(Measurement.date, Measurement.prcp).\
        order_by(Measurement.date).\
        all()

    session.close()
###########################################################
## CONVERSION TO DICTIONARIES ##

# Create a dictionary from the row data and append to a list of all_passengers
    Measurements_all = []
    for date, prcp in Measurement_qry:
        Measurement_dict = {}
        Measurement_dict["date"] = date
        Measurement_dict["prcp"] = prcp
        Measurements_all.append(Measurement_dict)

    return jsonify(Measurements_all)

######
######
#Stations Page
#Return list of unique stations
@app.route("/api/v1.0/stations/")
def Stations_list():
###########################################################
## QUERY ##
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of Date and Precipitation. Name dictionary as Measurement_dict"""
    # Query 
    distinct_stations_qry = session.query(distinct(Measurement.station)).all()

    session.close()

#############################################################
    return jsonify(distinct_stations_qry)

######
######
# Temperature of Obervations (TOBS) Page
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs/")
def tob_list():
###########################################################
## QUERY ##
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Station with highest number of TOBS (Temperature Observations): 'USC00519281'

    # Query for 1 yr ago from the latest_date
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    print("Query Date: ", query_date)

    #FOR station 'USC00519281' and only for data in latest year, query for a list which includes x-axis: Temps, y-axis: Frequency. 
    print("Query Date: ", query_date) #From 2016-08-23 (Query Date) to 2017-08-23

    freq_of_temps_qry = session.query(Measurement.station, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= query_date).\
        order_by((Measurement.tobs).asc()).all()

    session.close()

#############################################################
    return jsonify(freq_of_temps_qry)















#     #User entry in the website for the date in 
#     user_input = date.replace(" ", "")
#     # for d in Measurement_dict:
#     #     return jsonify(d)
        

# @app.route("/api/v1.0/justice-league/justice-league/superhero/<superhero>")
# def justice_league_character(superhero):
#     """Fetch the Justice League character whose superhero matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = superhero.replace(" ", "").lower() #From API, what user enters in the website
#     for character in justice_league_members:
#         search_term = character["superhero"].replace(" ", "").lower() #Changes letters in dictionary

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with superhero {superhero} not found."}), 404



#     # Convert list of tuples into normal list
#     # Measurement_list = list(np.ravel(Measurement_qry))

#     return jsonify(Measurement_dict)

# #     """Fetch the Justice League character whose real_name matches
# #        the path variable supplied by the user, or a 404 if not."""

# #     canonicalized = real_name.replace(" ", "").lower() #From API, what user enters
# #     for character in justice_league_members:
# #         search_term = character["real_name"].replace(" ", "").lower() #Changes letters in dictionary

# #         if search_term == canonicalized:
# #             return jsonify(character)

# #     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404








# #Convert the query results to a dictionary using date as the key and prcp as the value.
# # Measurement_yr = session.query(Measurement.date, Measurement.prcp).\
# #     filter(Measurement.date >= query_date).\
# #     order_by(Measurement.date).\
# #     all()
# #print(Measurement_yr)


# # # Create our session (link) from Python to the DB
# # session = Session(engine)
# # ]


if __name__ == "__main__":
    app.run(debug=True)
