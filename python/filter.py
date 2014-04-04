"""
   Retrieve information from database for a selected node.
"""
import flask, flask.views
from flask import jsonify
import logging
from flask import request
from flask import json
import dbHelper


class Filter(flask.views.MethodView):
    def __init__(self, dbConnection):
        self.db = dbConnection

    def post(self):
        """Return filtered data to front end in JSON format."""

        # Get filters that user has selected from AJAX request.
        # JSON encode string to make a python dictionary.
        filters = json.loads(request.data)
        data = self.filter_language_data(filters["data"])

        formatted_data = {"language_pairs": data}

        return jsonify({"value": data})

    def filter_language_data(self, language_filter):
        """
            Filter data based on currently selected languages.

            Taking all languages into account

            for each language selected
                find all occurrences of that language in data.
                so if Java is sent
                return all languages linking to Java
        """
        filtered_data = []
        if language_filter:

            db_data = dbHelper.get_language_data_from_db(self.db)
            for language in language_filter:
                for pair in db_data:
                    language_connection = pair.get("connection")

                    if language == language_connection[0] or language == language_connection[1]:
                        filtered_data.append(pair)

        return filtered_data
