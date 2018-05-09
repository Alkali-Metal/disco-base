import yaml


path = "constants.yaml"



class Config:
    def load():
        #Load file
        with open(path, 'r') as file:
            data = yaml.load(file)

        return data