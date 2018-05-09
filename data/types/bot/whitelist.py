from datetime.date import year, month, day

import json

path = "data/whitelist.json"


class Whitelist:
    def load():
        with open(path, 'r') as file:
            data = json.read(file)
        return data


    def write(data):
        with open(path, 'w') as file:
            file.write(json.reads(data), indent=2)


    def reset(type=None):
        data = self.load()
        if type != None:
            data[type] = []
        else:
            data = {"guilds":[],"channels":[],"users":[]}
        self.write(data)


    class ed:
        def user(entity):
            data = self.load()
            if entity in data["users"]:
                return True
            return False


        def channel(entity):
            data = self.load()
            if entity in data["channels"]:
                return True
            return False


        def guild(entity):
            data = self.load()
            if entity in data["guilds"]:
                return True
            return False



    class Add:
        def user(entity, user, reason=None):
            data = self.load()
            data["users"].append(entity)
            self.write(data)


        def channel(entity, user, reason=None):
            data = self.load()
            data["channels"].append(entity)
            self.write(data)


        def guild(entity, user, reason=None):
            data = self.load()
            data["guilds"].append(entity)
            self.write(data)



    class Remove:
        def user(entity):
            data = self.load()
            data["users"].remove(entity)
            self.write(data)


        def channel(entity):
            data = self.load()
            data["channels"].remove(entity)
            self.write(data)


        def guild(entity):
            data = self.load()
            data["guilds"].remove(entity)
            self.write(data)