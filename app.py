#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
import datetime as dt
from datetime import datetime
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

#####################
# PRECIPITATION PAGE
#####################
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


################
# STATIONS PAGE
################
# Return list of unique stations
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


#########################################
# TEMPERATURE OF OBSERVATIONS (TOBS) PAGE
#########################################
# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs/")
def tob_list():
# ###########################################################
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

#####################################################
# USER START DATE TO END DATA DATE: TMIN, TMAX, TAVG
#####################################################

# Min, Max, Avg Temp for given Start Date Page
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start to end of date data range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
@app.route("/api/v1.0/<start>", methods = ["GET"])
def start_date_tmin_tmax_tavg(start):
###########################################################
## QUERY ##
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #user_startdate = dt.date(2011, 8, 23) 
    start = datetime.strptime(start, "%Y-%m-%d").date()

    min_tobs_startdate_qry = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        order_by((Measurement.tobs).asc()).all()
    
    max_tobs_startdate_qry = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        order_by((Measurement.tobs).asc()).all()


    avg_tobs_startdate_qry = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        order_by((Measurement.tobs).asc()).all()

    session.close()

################

    return jsonify(f"User specified start date: {start}, Min Temp (F): {min_tobs_startdate_qry}, \n Max Temp (F): {max_tobs_startdate_qry} \n Avg Temp (F): {avg_tobs_startdate_qry}")
 
    





# # Min, Max, Avg Temp for given Start and End Date Page
# @app.route("/api/v1.0/<start>/<end>")
# def tob_st_fin_list():

####################################################
# USER START DATE AND USER END DATE: TMIN, TMAX, TAVG
#####################################################

# Min, Max, Avg Temp for given Start Date Page
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
@app.route("/api/v1.0/<start>/<end>", methods = ["GET"])
def start_end_date_tmin_tmax_tavg(start, end):
###########################################################
## QUERY ##
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #user_startdate = dt.date(2011, 8, 23) 
    start = datetime.strptime(start, "%Y-%m-%d").date()
    end = datetime.strptime(end, "%Y-%m-%d").date()

# filter( and_(User. birthday <= '1988-01-17', User. birthday >= '1985-01-17'))

    min_tobs_startdate_qry = session.query(Measurement.station, Measurement.date, func.min(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        order_by((Measurement.tobs).asc()).all()
    
    max_tobs_startdate_qry = session.query(Measurement.station, Measurement.date, func.max(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        order_by((Measurement.tobs).asc()).all()


    avg_tobs_startdate_qry = session.query(func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start, Measurement.date <= end).\
        order_by((Measurement.tobs).asc()).all()

    session.close()

# ################

    return jsonify(f"User specified start date: {start} and end date: {end}, Min Temp (F): {min_tobs_startdate_qry}, \n Max Temp (F): {max_tobs_startdate_qry} \n Avg Temp (F): {avg_tobs_startdate_qry}")
 
    
















# #     #User entry in the website for the date in 
# #     user_input = date.replace(" ", "")
# #     # for d in Measurement_dict:
# #     #     return jsonify(d)
        

# # @app.route("/api/v1.0/justice-league/justice-league/superhero/<superhero>")
# # def justice_league_character(superhero):
# #     """Fetch the Justice League character whose superhero matches
# #        the path variable supplied by the user, or a 404 if not."""

# #     canonicalized = superhero.replace(" ", "").lower() #From API, what user enters in the website
# #     for character in justice_league_members:
# #         search_term = character["superhero"].replace(" ", "").lower() #Changes letters in dictionary

# #         if search_term == canonicalized:
# #             return jsonify(character)

# #     return jsonify({"error": f"Character with superhero {superhero} not found."}), 404



# #     # Convert list of tuples into normal list
# #     # Measurement_list = list(np.ravel(Measurement_qry))

# #     return jsonify(Measurement_dict)

# # #     """Fetch the Justice League character whose real_name matches
# # #        the path variable supplied by the user, or a 404 if not."""

# # #     canonicalized = real_name.replace(" ", "").lower() #From API, what user enters
# # #     for character in justice_league_members:
# # #         search_term = character["real_name"].replace(" ", "").lower() #Changes letters in dictionary

# # #         if search_term == canonicalized:
# # #             return jsonify(character)

# # #     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404








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
