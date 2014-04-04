"""
   Retrieve information from database for a selected node
"""
from operator import itemgetter
import logging

import flask, flask.views
from flask import jsonify
from flask import request
from flask import json

import dbHelper

class Details(flask.views.MethodView):
    def __init__(self, dbConnection):
        self.db = dbConnection

    def post(self):
        """Return filtered data to front end in JSON format."""

        # Get clicked node that user has selected from AJAX request.
        # JSON encode string to make a python dictionary.
        selected_node = json.loads(request.data)
        node_data = self.get_node_details(selected_node["data"])
        formatted_data = {"language_pairs": node_data}

        return jsonify({"value": formatted_data})

    def get_node_details(self, language):
        """
            Retrieve nodes associated with selected language.

            Arguments:
                * language: language node clicked.


            Returns:
                * Node information for selected language.
        """

        filtered_data = []
        db_data = dbHelper.get_language_data_from_db(self.db)

        for pair in db_data:
            language_connection = pair.get("connection")

            if language == language_connection[0] or language == language_connection[1]:
                filtered_data.append(pair)

        # First element of sorted_data is most popular
        sorted_data = sorted(filtered_data, key=itemgetter('count'), reverse=True)

        return sorted_data
