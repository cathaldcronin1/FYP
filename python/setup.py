"""
    Startup script to perform first time set up of:

    * All interactions with GitHub.
    * Retrieving storing and formatting data from GitHub.
    * First time set up of database.

    Above to be performed when application starts.
"""
from requests.auth import HTTPBasicAuth
import requests

class Setup():
    """
        Performs all setup operations for application.

        If database exists script doesn't need to execute.
        otherwise performs initialisation.
    """

    def __init__(self, connection):
        self.public_users_url = "https://api.github.com/users"
        self.auth = HTTPBasicAuth('cathaldcronin1', 'Zelda#0018')

        print connection["app23744423"]["language_connections"]
        self.client = connection["app23744423"]
        self.db = self.client
        self.language_connections = self.db.language_connections
        self.languages = self.db.languages

        # Check if database is populated with information.
        setup = self.isSetup(self.client)

        if not setup:
            print "Performing First Time Setup"
            language_connections_data, languages_data = self.gather_language_information()

            # Store data retrieved from GitHub in database.
            for connection in language_connections_data:
                connection_id = self.language_connections.insert(connection)

            language_id = self.languages.insert({'languages': languages_data})
        else:
            print "Setup Already Performed"

    def get_languages_per_user(self, repo_urls):
        """
            Each URL in repo_urls contains repository information
            for a single user.

            Each URL requested returns a JSON object which is parsed
            for the primary pieces of information.

            Arguments:
                * repo_urls: list of repository URLs.

            Returns:
                * A list of dictionaries containing the primary information for each users repository

        """

        language_info = []
        for url in repo_urls:
            user_repo = requests.get(url, auth=self.auth).json()

            # Now have a JSON structure of a users repository.
            # Pull out the primary "language" of each repository
            language_list = []
            for repo in user_repo:

                # Now iterating through each users repos.
                # Pull out repoName, primary language,
                repo_name = repo.get("name")
                language =  repo.get("language")

                # Handle case where null language exists!
                if language:
                    language_list.append(language)

            # A user may have multiple projects that are the same language.
            # Only need to keep track of each language once.
            # Remove duplicates from the list of languages.
            normalised_languages = list(set(language_list))

            language_info.append({"name" : repo_name,
                                  "languages": normalised_languages,}
                                )

        return language_info

    def make_language_pairs(self, language_info):
        """
            A list of language pairs are created for each set of languages found per user.

            Arguments:
                * language_info: List of dictionaries containing
                    a users name and the list of languages found for that users repository.

                * A pairing is created between every language found in the list of languages for a user.

                    E.g.
                        [{"Joe Blogs": ['Python', 'Java', 'Ruby'],...}

            Returns:
                * A list of tuples.

                    E.g
                        [('Python', 'Ruby'),...]
        """

        pairs = []
        for user in language_info:
            languages = user["languages"]
            i = 0
            while i < len(languages):
                j = 1 + i
                while j < len(languages):

                    # If languages are the same, move on
                    if languages[i] == languages[j]:
                        continue

                    # Make pair.
                    pair = [languages[i], languages[j]]
                    pairs.append(pair)
                    j += 1
                i+=1

        return pairs

    def make_language_mappings(self, language_pairs):
        """
            A list of dictionaries is created containing a language pair and
            a count of the number of occurrences of that pairing.

            Arguments:
                * language_pairs: A list containing every pair of languages.

            Returns:
                * language_mapping: list of dictionaries

                    E.g
                    [{'count': 27, connection: [Python: Ruby]}...]
        """

        pairs = language_pairs
        language_mapping = []

        for pair in pairs:

            # Count occurrences of pairings
            count = pairs.count(pair)

            # Count swapped pairings
            swapped_pair = [pair[1], pair[0]]
            swappd_count = pairs.count(swapped_pair)

            total_count = count + swappd_count
            pair_to_add = pair

            # Update list of pairs
            updated_pairs = self.remove_values_from_list(pairs, pair)

            # remove swapped pairs
            updated_pairs = self.remove_values_from_list(updated_pairs, swapped_pair)

            pairs = updated_pairs

            if count != 0:
                language_mapping.append({"count": total_count,
                                         "connection": pair_to_add})

        return language_mapping

    def gather_language_information(self):
        """
            Perform all initialisation steps required for application.

            1. Retrieve a list of user on GitHub.
            2. For each user, gather their repository information.
                2.1. Create a list of languages found per user.
            3. Make a list of pairs of all languages
            4. Count occurrences of pairings.
            5. Format occurrences with pairings.
            6. Store formatted data in the database.

            Returns:
                Normalised list of languages found.
                List of dictionaries containing pairs and occurrences of each pair.
        """

        # Get public GitHub users.
        github_users = requests.get(self.public_users_url, auth=self.auth).json()

        # Get URL for users repos.
        repo_urls = []
        for user in github_users:
            repo_urls.append(user.get("repos_url"))

        # Generate list of languages per user.
        language_info = self.get_languages_per_user(repo_urls)

        # Make pairs of languages.
        pairs = self.make_language_pairs(language_info)

        # Count occurrences of each language pair.
        language_mapping = self.make_language_mappings(pairs)

        # make languages list
        languages = self.get_list_of_languages(language_mapping)

        return language_mapping, languages

########################################

#           Helper Methods             #

########################################

    def remove_values_from_list(self, the_list, val_to_remove):
        """
            Returns a new list where all occurrences of val_to_remove
            have been removed from the_list

            Arguments:
                * the_list : list of languages.
                * val_to_remove: value to remove from list.

            Returns:
                * A new list where the value has been removed.
        """
        return [value for value in the_list if value != val_to_remove]

    def get_list_of_languages(self, language_connections):
        """
            Make a list of languages given a  set of pairs

            Arguments:
                * language_connections: A list of in the form:
                    [{'count': 29, 'connection': [u'Shell', u'Ruby']},
                    {'count': 26, 'connection': [u'Python', u'Ruby']}]

            Returns:
                * Normalised list of languages.
        """
        languages = []

        for pair in language_connections:

            # Get language pair
            lang1 = pair["connection"][0]
            lang2 = pair["connection"][1]

            languages.append(lang1)
            languages.append(lang2)

        return list(set(languages))

    def isSetup(self, client):
        """
            Check if database exists or not.

            Arguments:
                * client: MongoDB connection

            Returns:
                * Boolean value if database exits or not.
        """
        # databases = client.database_names()
        # if "language_database" in databases:
            # return True
        # else:
        return False
