# BOT IMPORTS:
from data.constants import (
    DB_indent_level,
    base_JSON_path
)

# DISCO IMPORTS:

# MISC IMPORTS:
import json


#=============================================================================#
# MAIN HANDLER:


class JSON:
    """
    The custom JSON handler that all of the other handlers extend
    """



    def load(file):
        """
        Loads a JSON file at the base path given.

        @file - The filename of the file wanting to load
        """
        
        # Ensure file ends with .json
        if not file.endswith(".json"):
            file + ".json"

        # Open the file safely
        with open(base_JSON_path + file, 'r') as file:
            return json.load(file)
    


    def write(file, data):
        """
        Writes to the specified JSON file overwriting all other contents.

        @file - The filename of the file wanting to load
        @data - The object to stringify and replace the contents of the file
                 with
        """

        # Ensure file ends with .json
        if not file.endswith(".json"):
            file + ".json"


        # Write to the file
        with open(base_JSON_path + file, 'w') as file:
            file.write(json.dumps(data, indent=DB_indent_level))