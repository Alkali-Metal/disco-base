import json


path = "config.json"



class Config:
    def load():
        #Load file
        with open(path, 'r') as file:
            data = json.load(file)

        return data