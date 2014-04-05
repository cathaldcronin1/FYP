"""
    Overview of languages information.
    All langugae data is formatted and sent to the frontend of the system.
"""
import flask, flask.views
from flask import jsonify
import dbHelper

class GraphData(flask.views.MethodView):
    def __init__(self, dbConnection):
        self.db = dbConnection

    def get(self):
        data = self.gather_information()
        return data

    def gather_information(self):
        """
            Gather Information from GitHub and send to frontend.

            Arguments:
                * None.

            Returns:
                * Overview graph data to frontend in JSON format.

                E.g [{'count': 29, 'connection': [u'Shell', u'Ruby']},
                     {'count': 26, 'connection': [u'Python', u'Ruby']}]
        """

        # Get database information
        language_connection_data, count_values = dbHelper.get_language_data_from_db(self.db)
        languages = self.db['languages']
        languages_data = list(languages.find())
        languages_data = languages_data[0].get("languages")

        min_count = min(count_values)
        max_count = max(count_values)

        # Data to send to frontend
        data =  {"language_pairs": language_connection_data,
                 "languages": languages_data,
                 "min_count": min_count,
                 "max_count": max_count}

        return jsonify({"value": data})
