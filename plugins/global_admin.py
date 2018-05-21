# BOT IMPORTS:
from data.types.bot.plugin_config import PluginConfig
from data.types.bot.config import Config
from data.response import GlobalAdmin

# DISCO IMPORTS:
from disco.bot import Plugin



class GlobalAdministration(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = True
    bypass_enabled = True
    can_be_enabled = False
    plugin_version = 2.0
    config_settings = {}

    commands_config = {
        "plugin": {
            "enable": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 4,
                "bypass_user_perms": False
            },
            "disable": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 4,
                "bypass_user_perms": False
            },
            "list": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 2,
                "bypass_user_perms": False
            }
        },
        "guild": {
            "enable": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 4,
                "bypass_user_perms": False
            }
        }
    }
    #=======================================#

#=============================================================================#
# COMMANDS:


    @Plugin.command("enable", group="plugin")
    def plugin_enable(self, event):



        #argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = event.args[0]
        plugin = event.args[1]


        #is using "self" argument?
        if guild_id.lower() == "self":

            # Ensure a guild exists
            if event.guild:
                guild_id = str(event.msg.guild.id)
            else:
                return event.msg.reply(GlobalAdmin.arg.format(guild_id))


        #ensure the plugin exists
        if plugin not in self.bot.plugins.keys():

            return event.msg.reply(
                GlobalAdmin.invalid_plugin.format(
                    plugin
                )
            )
        else:
            plugin = self.bot.plugins[plugin]

        #ensure the plugin is allowed to be enabled
        if not plugin.can_be_enabled:
            return event.msg.reply(
                GlobalAdmin.cannot_be_enabled.format(
                    plugin
                )
            )

        config = PluginConfig.load("guild_list")

        #plugin enabled already?
        if plugin.name not in config[guild_id]:
            config[guild_id].append(plugin.name)
            PluginConfig.write("guild_list", config)
            return event.msg.reply(
                GlobalAdmin.added_plugin.format(
                    plugin.name,
                    guild_id
                )
            )
        else:
            return event.msg.reply(
                GlobalAdmin.plugin_already_enabled.format(
                    guild_id,
                    plugin.name
                )
            )
        
    


    @Plugin.command("disable", group="plugin")
    def plugin_disable(self, event):


        #argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = event.args[0]
        plugin = event.args[1]

        #is using "self" argument?
        if guild_id.lower() == "self":
            if event.guild:
                guild_id = str(event.msg.guild.id)
            else:
                return event.msg.reply(GlobalAdmin.arg.format(guild_id))

        #ensure the plugin exists
        if plugin not in self.bot.plugins.keys():
            return event.msg.reply(
                GlobalAdmin.invalid_plugin.format(
                    plugin
                )
            )
        plugin = self.bot.plugins[plugin]

        #ensure the plugin is allowed to be enabled
        if not plugin.can_be_enabled:
            return event.msg.reply(
                GlobalAdmin.cannot_be_enabled.format(
                    plugin
                )
            )

        config = PluginConfig.load("guild_list")

        #plugin enabled?
        if plugin in config[guild_id]:
            config[guild_id].remove(plugin)
            event.msg.reply(
                GlobalAdmin.removed_plugin.format(
                    plugin,
                    guild_id
                )
            )
            #update file
            PluginConfig.write("guild_list", config)
        else:
            #acknowledge error
            event.msg.reply(
                GlobalAdmin.plugin_not_enabled.format(
                    guild_id,
                    plugin
                )
            )



    @Plugin.command("list", group="plugin")
    def plugin_list(self, event):


        #ensure the user supplies at least one argument
        if len(event.args) < 1:
            return event.msg.reply(GlobalAdmin.nea)
        
        #check if the guild_id is self
        if event.args[0].lower() == "self":
            if event.guild:
                guild_id = str(event.msg.guild.id)
            else:
                return event.msg.reply(GlobalAdmin.arg.format(guild_id))
        else:
            guild_id = event.args[0]


        try:
            #loading the guild's plugins
            plugins = PluginConfig.load("guild_list")[guild_id]
        except KeyError:
            return event.msg.reply(GlobalAdmin.invalid_arg.format(guild_id))


        #convert arguments if given
        try:
            #end only
            if len(event.args) == 2:
                start = 0
                end = int(event.args[1])

            #both
            elif len(event.args) == 3:
                start = int(event.args[1])
                end = int(event.args[2])

            #no arguments given
            else:
                start = 0
                end = len(plugins)

        #invalid integer given
        except ValueError:
            return event.msg.reply(GlobalAdmin.invalid_int)

        #Ensure start is not greater than end
        if (start - end) > 0:
            return event.msg.reply(GlobalAdmin.error)
        #Start == end (meaning no plugins to list)
        elif (start - end) == 0:
            return event.msg.reply(
                GlobalAdmin.no_list_zero.format(
                    "plugins"
                )
            )

        #Ensure user's "start" is lower than highest index
        if start > (len(plugins) - 1):
            return event.msg.reply(
                GlobalAdmin.start_too_big.format(
                    len(plugins) - 1
                )
            )

        response = GlobalAdmin.plugin_list.format(
            guild_id,
            ", ".join(plugins[start:end])
        )

        #Ensure message length
        if len(response) > 2000:
            return event.msg.reply(GlobalAdmin.message_too_long)

        #acknowledge
        event.msg.reply(response)



    @Plugin.command("enable", group="guild", aliases=["whitelist"])
    def guild_enable(self, event):


        guild_list = PluginConfig.load("guild_list")

        #check if arguments used
        if len(event.args) >= 1:
            guild_id = event.args[0]
        else:
            if event.guild:
                guild_id = str(event.guild.id)
            else:
                return event.msg.reply(GlobalAdmin.nea)
        
        #"self" argument used
        if guild_id.lower() == "self":
            guild_id = str(event.msg.guild.id)

        #ensure guild not enabled
        if guild_id in guild_list.keys():
            return event.msg.reply(
                GlobalAdmin.guild_already_enabled.format(
                    guild_id
                )
            )

        #Add guild to file
        try:
            guild_list[guild_id] = []
            PluginConfig.write("guild_list", guild_list)
        except:
            return event.msg.reply(GlobalAdmin.error)

        event.msg.reply(
            GlobalAdmin.guild_enabled.format(
                guild_id
            )
        )



    @Plugin.command("disable", group="guild")
    def guild_disable(self, event):


        guild_list = PluginConfig.load("guild_list")

        #check if arguments used
        if len(event.args) >= 1:
            guild_id = event.args[0]
        else:
            return event.msg.reply(GlobalAdmin.nea)
        
        #"self" argument used
        if guild_id.lower() == "self":
            if event.guild:
                guild_id = str(event.msg.guild.id)
            else:
                return event.msg.reply(GlobalAdmin.arg.format(guild_id))

        #ensure guild not enabled
        if guild_id not in guild_list.keys():
            return event.msg.reply(
                GlobalAdmin.guild_not_enabled.format(
                    guild_id
                )
            )

        #Add guild to file
        try:
            guild_list.pop(guild_id)
            PluginConfig.write("guild_list", guild_list)
        except:
            return event.msg.reply(GlobalAdmin.error)

        event.msg.reply(
            GlobalAdmin.guild_disabled.format(
                guild_id
            )
        )



    @Plugin.command("list", group="guild")
    def guild_list(self, event):


        #loading the guild list
        guild_list = PluginConfig.load("guild_list")

        #convert arguments if given
        try:
            #end only
            if len(event.args) == 1:
                start = 0
                end = int(event.args[0])
            
            #both
            elif len(event.args) == 2:
                start = int(event.args[0])
                end = int(event.args[1])

            #no arguments given
            else:
                start = 0
                end = len(guild_list)

        #invalid integer given
        except ValueError:
            return event.msg.reply(GlobalAdmin.invalid_int)


        #Ensure start is not greater than end
        if (start - end) > 0:
            return event.msg.reply(GlobalAdmin.error)

        #Start == end (meaning no guilds to list)
        elif (start - end) == 0:
            return event.msg.reply(
                GlobalAdmin.no_list_zero.format(
                    "guilds"
                )
            )

        #Ensure user's "start" is lower than highest index
        if start > (len(guild_list) - 1):
            return event.msg.reply(
                GlobalAdmin.start_too_big.format(
                    len(guild_list) - 1
                )
            )

        response = GlobalAdmin.guild_list.format(
            ", ".join(list(guild_list.keys())[start:end])
        )

        #Ensure message length
        if len(response) > 2000:
            return event.msg.reply(GlobalAdmin.message_too_long)

        #acknowledge
        event.msg.reply(response)