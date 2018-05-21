import json

from data.types.bot.exceptions import PluginError

from data.types.discord.logger import Log

from os import listdir


base_path = "data/"


class PluginConfig:
    def load(name):
        if not name.endswith(".json"):
            name = name + ".json"
        try:
            with open(base_path + name, 'r') as file:
                data = json.load(file)
            return data
        except:
            PluginError("Plugin config cannot be found.")



    def write(name, data):
        if not name.endswith(".json"):
            name = name + ".json"
        with open(base_path + name, 'w') as file:
            file.write(json.dumps(data, indent=2))
    
    
    
    def exists(name):
        files = []
        for file in listdir(base_path):
            if file.endswith(format):
                files.append(file)

        if not name.endswith(".json"):
            name = name + ".json"

        if name in files:
            return True
        else:
            return False