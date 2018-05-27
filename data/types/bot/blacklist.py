import json
from datetime import date


path = "data/blacklist.json"


class Blacklist():
    def load():
        with open(path, 'r') as file:
            data = json.load(file)
        return data


    def write(data):
        with open(path, 'w') as file:
            file.write(json.loads(data), indent=2)


    def get(type, entity):
        data = Blacklist.load()
        data = [data[type][entity]["by"],
                data[type][entity]["reason"],
                data[type][entity]["on"]]
        return data


    def reset(type=None):
        data = Blacklist.load()
        if type != None:
            data[type] = {}
        else:
            data = {"guilds":{},"channels":{},"users":{}}
        Blacklist.write(data)


    class ed:
        def user(entity):
            data = Blacklist.load()
            if entity in data["users"]:
                return True
            return False


        def channel(entity):
            data = Blacklist.load()
            if entity in data["channels"]:
                return True
            return False


        def guild(entity):
            data = Blacklist.load()
            if entity in data["guilds"]:
                return True
            return False



    class Add:
        def user(entity, user, reason=None):
            data = Blacklist.load()

            # Get date
            year = date.year
            month = date.month
            day = date.day

            # Add entitiy to blacklist
            data["users"][entity] = {
                "reason":reason,
                "by": user,
                "on": "{}/{}/{}".format(year, month, day)
            }

            Blacklist.write(data)


        def channel(entity, user, reason=None):
            data = Blacklist.load()

            # Get date
            year = date.year
            month = date.month
            day = date.day

            # Add entity            
            data["channels"][entity] = {
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
            year = date.year
            month = date.month
            day = date.day

            # Add entity
            data["guilds"][entity] = {
                "reason":reason,
                "by": user,
                "on": "{}/{}/{}".format(year, month, day)
            }
            Blacklist.write(data)



    class Remove:
        def user(entity):
            data = Blacklist.load()
            data["users"].pop(entity)
            Blacklist.write(data)


        def channel(entity):
            data = Blacklist.load()
            data["channels"].pop(entity)
            Blacklist.write(data)


        def guild(entity):
            data = Blacklist.load()
            data["guilds"].pop(entity)
            Blacklist.write(data)