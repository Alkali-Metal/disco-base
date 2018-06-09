# BOT IMPORTS:
from data.constants import (
    base_JSON_path
)
from util.json_handler import JSON

# DISCO IMPORTS:

# MISC IMPORTS:
from datetime import date
from os import listdir

today = date.today

#=============================================================================#
# VARIABLE INITIALIZATION:
config_dir = "guilds/"
default_guild = ".static-json/default_guild_template.json"


#=============================================================================#
# HANDLER EXTENSION:


class Blacklist:



    def load():
        """
        Loads a JSON file from the data/plugin-config directory
        """

        return JSON.load("blacklist.json")



    def write(data):
        """
        Writes to a JSON file from the data/plugin-config directory
        """

        return JSON.write("blacklist.json", data)


    def get(type, entity):
        data = Blacklist.load()
        data = [
            data[type][entity]["by"],
            data[type][entity]["reason"],
            data[type][entity]["on"]
        ]
        return data



    def reset(type=None):
        data = Blacklist.load()
        if type != None:
            data[type] = {}
        else:
            data = {"guild":{},"channel":{},"user":{}}
        Blacklist.write(data)



    class ed:
        def user(entity):
            data = Blacklist.load()

            # See if entity in dict
            if entity in data["user"]:

                # Ensure entity isn't a global admin

                return True
            return False



        def channel(entity):
            data = Blacklist.load()
            if entity in data["channel"]:
                return True
            return False



        def guild(entity):
            data = Blacklist.load()
            if entity in data["guild"]:
                return True
            return False



    class Add:
        def user(entity, user, reason=None):
            data = Blacklist.load()

            # Get date
            year = today().year
            month = today().month
            day = today().day

            # Add entitiy to blacklist
            data["user"][entity] = {
                "reason":reason,
                "by": user,
                "on": "{}/{}/{}".format(year, month, day)
            }

            Blacklist.write(data)



        def channel(entity, user, reason=None):
            data = Blacklist.load()

            # Get date
            year = today().year
            month = today().month
            day = today().day

            # Add entity            
            data["channel"][entity] = {
                "reason":reason,
                "by": user,
                "on": "{}/{}/{}".format(
                    year,
                    month,
                    day
                )
            }
            Blacklist.write(data)



        def guild(entity, user, reason=None):
            data = Blacklist.load()

            # Get date
            year = today().year
            month = today().month
            day = today().day

            # Add entity
            data["guild"][entity] = {
                "reason":reason,
                "by": user,
                "on": "{}/{}/{}".format(year, month, day)
            }
            Blacklist.write(data)



    class Remove:
        def user(entity):
            data = Blacklist.load()
            data["user"].pop(entity)
            Blacklist.write(data)



        def channel(entity):
            data = Blacklist.load()
            data["channel"].pop(entity)
            Blacklist.write(data)



        def guild(entity):
            data = Blacklist.load()
            data["guild"].pop(entity)
            Blacklist.write(data)