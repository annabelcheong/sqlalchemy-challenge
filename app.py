#Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<br/>"
        f"/api/v1.0/passengers"
    )

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

#     @app.route("/api/v1.0/precipitation/<date>")
# def precip_data(date):
#     """Fetch the Justice League character whose real_name matches
#        the path variable supplied by the user, or a 404 if not."""

#     canonicalized = real_name.replace(" ", "").lower() #From API, what user enters
#     for character in justice_league_members:
#         search_term = character["real_name"].replace(" ", "").lower() #Changes letters in dictionary

#         if search_term == canonicalized:
#             return jsonify(character)

#     return jsonify({"error": f"Character with real_name {real_name} not found."}), 404








#Convert the query results to a dictionary using date as the key and prcp as the value.
# Measurement_yr = session.query(Measurement.date, Measurement.prcp).\
#     filter(Measurement.date >= query_date).\
#     order_by(Measurement.date).\
#     all()
#print(Measurement_yr)


# # Create our session (link) from Python to the DB
# session = Session(engine)
# ]


if __name__ == "__main__":
    app.run(debug=True)
