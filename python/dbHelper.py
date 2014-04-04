def get_language_data_from_db(connection):
    """
        Return formatted language information from database.

        Arguments:
            * connection: MongoDB database connection.

        Returns:
            * language_connection_data: All language information from database.
    """

    language_db = connection['language_database']
    language_pairs = language_db['language_connections']

    # Cast database object to a list to iterate through it.
    db_langauge_data = list(language_pairs.find())

    language_connection_data = []

    for pair in db_langauge_data:
        count = pair.get("count")
        connection = pair.get("connection")

        language_connection_data.append({"count": count, "connection": connection})

    return language_connection_data
