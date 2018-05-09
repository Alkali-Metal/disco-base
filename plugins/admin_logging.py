class AdminLogging(Plugin):

    # guild added to bot
    @Plugin.listen("GuildCreate")
    def on_guild_create(self, event):
        if event.unavailable == None:

            # load master configs
            guild_list = PluginConfig.load("guild_list.json")
            config = Config.load()

            guild_id = str(event.guild.id)


            # create enabled list if not already existed
            if guild_id not in guild_list:
                guild_list[guild_id] = []
                PluginConfig.write("guild_list.json", guild_list)
                
                # log event
                Logging.INFO()
    


    # bot removed from guild
    @Plugin.listen("GuildDelete")
    def on_guild_delete(self, event):
        if event.unavailable == None:

            # load master configs
            guild_list = PluginConfig.load("guild_list.json")
            config = Config.load()

            guild_id = str(event.guild.id)

            # create enabled list if not already existed
            if not guild_id in guild_list:
                guild_list[guild_id] = []
                PluginConfig.write("guild_list.json", guild_list)
                
                # log event
                Logging.INFO()