"""
    Application Setup involves:
        * MongoDB Server Start up.
        * Populating Database.
        * Defining URL routes.

    Each URL route maps a URL of the application to a back-end python function
"""
import os
import subprocess

import flask, flask.views
from pymongo import MongoClient

from python.main import Main
from python.graph import GraphData
from python.shutdown import Shutdown
from python.setup import Setup
from python.filter import Filter
from python.details import Details
from python.refresh import Refresh


# MongoDB server startup
# Establish connection to MongoDB
MONGO_URL = os.environ['MONGOHQ_URL']
connection = MongoClient(MONGO_URL)

# Get database
database = connection.language_database

# Create Flask Instance and set PORT
app = flask.Flask(__name__)

# Perform First time setup
setup = Setup(connection)

# URL Route definitions #

# Main Page Routes.
app.add_url_rule('/',
                 view_func=Main.as_view('main'),
                 methods=["GET"])

# Graph Overview.
app.add_url_rule('/_gather_graph_data',
                 view_func=GraphData.as_view('graphOverview', database),
                 methods=["GET"])

# Filter Data.
app.add_url_rule('/_filter_data',
                 view_func=Filter.as_view('filter', database),
                 methods=["POST"])

# Node Details.
app.add_url_rule('/_get_node_details',
                 view_func=Details.as_view('details', database),
                 methods=["POST"])

# Shutdown server.
app.add_url_rule('/shutdown',
                 view_func=Shutdown.as_view('shutdown'),
                 methods=["GET"])

# Refresh Data.
app.add_url_rule('/_refresh_data',
                 view_func=Refresh.as_view('refresh', connection, setup),
                 methods=["GET"])

# Gracefully Handle 404 error.
@app.errorhandler(404)
@app.errorhandler(503)
def page_not_found(error):
    return flask.render_template('404.html'), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
