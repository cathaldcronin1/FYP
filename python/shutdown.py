"""
    Shutdown view file. Returns shutdown html file that is rendered for the user.
"""

import flask, flask.views

class Shutdown(flask.views.MethodView):
    def get(self):
        """Server will shutdown, renders shutdown.html before hand"""
        self.shutdown_server()
        return flask.render_template("shutdown.html")

    def shutdown_server(self):
        """Shutsdown Flask server."""
        shutdown = flask.request.environ.get('werkzeug.server.shutdown')
        if shutdown is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        shutdown()
