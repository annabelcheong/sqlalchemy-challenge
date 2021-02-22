#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import distinct
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
