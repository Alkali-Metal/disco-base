from data.types.bot.plugin_config import PluginConfig

from os import listdir

import json


guild_config_path = "data/guilds/"
default_guild_config = "default_guild_template.json"


class GuildConfig:


    def load(guild_id, force_guild=False, no_guild_default=True):
        guild_id = str(guild_id)

        #check for filetype
        if not guild_id.endswith(".json"):
            guild_config = str(guild_id) + ".json"

        data = None

        #check if it exists
        if GuildConfig.exists(guild_id):
            with open(guild_config_path + guild_config, 'r') as file:
                data = json.load(file)
        
        #otherwise load defaults
        else:

            #see if we are forcing a guild config
            if force_guild:
                data = GuildConfig.create(guild_id, give_back=True)
            elif no_guild_default:
                with open(guild_config_path + "default.json", 'r') as file:
                    data = json.load(file)
        return data



    def write(guild_id, data):
        guild_id = str(guild_id)

        #check for filetype
        if not guild_id.endswith(".json"):
            guild_config = str(guild_id) + ".json"
        
        #check if the config exists
        if GuildConfig.exists(guild_id):
            with open(guild_config_path + guild_config, 'w') as file:
                file.write(json.dumps(data, indent=2))



    def create(guild_id, give_back=False):

        #make sure it doesn't exist
        if not GuildConfig.exists(guild_id):
            with open(guild_config_path + str(guild_id) + ".json", 'w') as data:
                data = PluginConfig.load(default_guild_config)
            GuildConfig.write(guild_id, data)

            #send back the data if requested
            if give_back:
                return data



    def reset(guild_id):
        guild_id = str(guild_id)

        #make sure the guild exists
        if GuildConfig.exists(guild_id):
            data = GuildConfig.load(guild_id)
            data = {}
            GuildConfig.write(data)



    def exists(guild_id):
        file_list = listdir(guild_config_path)
        guild_id = str(guild_id)

        #check for filetype
        if not guild_id.endswith(".json"):
            guild_config = str(guild_id) + ".json"
        
        #guild file in the list
        if guild_config in file_list:
            return True
        else:
            return False