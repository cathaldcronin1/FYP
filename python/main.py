"""
    Main view file. Returns main HTML file that is rendered for the user.
    If index.html is not available a 404 error is thrown and handled.
"""
import os

import flask, flask.views

class Main(flask.views.MethodView):
    def get(self, page="index"):
        """
            GET request response returns index.html to be rendered

            Arguments:
                * page: string of html page to be returned.

            Returns:
                * index.html or 404.html if not available.
        """

        page += ".html"
        if os.path.isfile('templates/' + page):
            return flask.render_template(page)
        flask.abort(404)
