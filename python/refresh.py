"""
    Script to refresh data stored in database.
"""
import flask, flask.views
from flask import jsonify

class Refresh(flask.views.MethodView):
    def __init__(self, dbConnection, setup):
        self.db = dbConnection
        self.setup = setup

    def get(self):
        """ """
        data = self.refresh_data()
        return data


    def refresh_data(self):
        """ """
        # Drop tables
        self.db.language_connections.drop()
        self.db.languages.drop()

        # re-setup again.
        language_connections_data, languages_data = self.setup.gather_language_information()

        # Store refreshed data retrieved from GitHub in database.
        for connection in language_connections_data:
            connection_id = self.db.language_connections.insert(connection)

        language_id = self.db.languages.insert({'languages': languages_data})


        return jsonify({"value": "True"})

