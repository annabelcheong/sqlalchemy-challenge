#Dependencies
from flask import Flask, jsonify

#LIST ALL THE DICTIONARIES HERE#######
#precip_data= [




# ]


############

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# @app.route("/api/v1.0/justice-league")
# def justice_league():
#     """Return the justice league data as json"""

#     return jsonify(justice_league_members)

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

    @app.route("/api/v1.0/precipitation/<date>")
def precip_data(date):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    canonicalized = real_name.replace(" ", "").lower() #From API, what user enters
    for character in justice_league_members:
        search_term = character["real_name"].replace(" ", "").lower() #Changes letters in dictionary

        if search_term == canonicalized:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
