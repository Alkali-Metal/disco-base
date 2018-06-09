# BOT IMPORTS:
from data.constants import (
    base_JSON_path
)
from util.json_handler import JSON

# DISCO IMPORTS:

# MISC IMPORTS:
from os import listdir


#=============================================================================#
# VARIABLE INITIALIZATION:
config_dir = "plugin-configs/"


#=============================================================================#
# HANDLER EXTENSION:


class PluginConfig:



    def load(name):
        """
        Loads a JSON file from the data/plugin-config directory
        """

        # Ensure filetype
        if not name.endswith(".json"):
            name = name + ".json"

        return JSON.load(config_dir + name)



    def write(name, data):
        """
        Writes to a JSON file from the data/plugin-config directory
        """

        # Ensure filetype
        if not name.endswith(".json"):
            name = name + ".json"

        return JSON.write(config_dir + name, data)



    def exists(name):
        """
        Checks if a plugin configuration exists, returns a boolean
        """

        files = []

        # Cycle through files in directory
        for file in listdir(base_JSON_path + config_dir):
            if file.endswith(".json"):
                files.append(file)

        # Ensure filetype
        if not name.endswith(".json"):
            name = name + ".json"

        return (name in files)