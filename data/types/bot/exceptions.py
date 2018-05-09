#The custom exceptions used by the bot


#errors to do with plugins
class PluginError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



#errors to do with logging
class LoggingError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)