"""
Commands that allow global administrators to adminstrate the guilds and plugins
of the bot.

TODO:
    !plugin <install|delete|add|remove>
    !blacklist <list|reset>
"""
# BOT IMPORTS:
from data.types.discord.embeds import BlacklistInfoEmbed
from data.types.bot.plugin_config import PluginConfig
from data.types.bot.blacklist import Blacklist
from data.types.bot.permissions import Perms
from data.types.bot.config import Config
from data.response import GlobalAdmin
from data.constants import (
    valid_blacklists,
    perm_ints
)

# DISCO IMPORTS:
from disco.bot import Plugin


#=============================================================================#
# FUNCTIONS:

def convert_guild_self(arg, msg):

    # Is using "self" argument?
    if arg.lower() == "self":

        # Ensure a guild exists
        if msg.guild != None:
            return str(msg.guild.id)

        # Error if no guild present
        else:
            return 
    
    # Return what we were given
    return arg



def filter_plugins(plugins, guild_plugins, start, stop):
    response = ""

    # Cycle through all plugins in bot
    for plugin in list(plugins.keys())[start:stop]:
        plugin = plugins[plugin]

        # Ensure the plugin can actually be enabled
        if plugin.can_be_enabled or plugin.bypass_enabled:

            # Check if the guild has it enabled
            if (plugin.name in guild_plugins):
                response = "{}\n+ {} V{}".format(
                    response,
                    plugin.name,
                    plugin.plugin_version
                )
            elif plugin.bypass_enabled:
                response = "{}\n* {} V{}".format(
                    response,
                    plugin.name,
                    plugin.plugin_version
                )
            else:
                response = "{}\n- {} V{}".format(
                    response,
                    plugin.name,
                    plugin.plugin_version
                )

            # Check if plugin is in development
            if plugin.in_dev:
                response = response + " DEV"

            # Check if plugin is restricted
            if plugin.restricted:
                response = response + " (Restricted)"
    
    return response



#=============================================================================#
# PLUGIN INITIALIZATION & CONFIGURATION:

class GlobalAdministration(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = True
    can_reload = True
    restricted = False
    force_default = True
    bypass_enabled = True
    can_be_enabled = False
    plugin_version = 0.2
    config_settings = {}
    plugin_info = [
        "Commands for global administrators to enable, disable, and list both",
        "guilds and their plugins. Also logs events: `ready`, `guild_create`,",
        "`guild_delete`, `guild_available`, `guild_unavailable` to the admin",
        "logging webhook."
    ]
    commands_config = {
        "plugin": {
            "enable": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}plugin enable",
                    "<Guild: Snowflake | `self`>",
                    "<Plugin: String>"
                ],
                "info": [
                    "Enables a plugin for the specified guild. If `self` is",
                    "used rather than a snowflake, it will enable the plugin",
                    "for whatever guild the command was run from within."
                ]
            },
            "disable": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}plugin disable",
                    "<Guild: Snowflake | `self`>",
                    "<Plugin: String>"
                ],
                "info": [
                    "Disables a plugin for the specified guild. If `self` is",
                    "used rather than a snowflake, it will disable the plugin",
                    "for whatever guild the command was run from within."
                ]
            },
            "list": {
                "DM_level": perm_ints["server_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["server_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}plugin list",
                    "<Guild: Snowflake | `self`>",
                    "[Start: Integer]",
                    "[Stop: Integer]"
                ],
                "info": [
                    "Lists all plugins enabled within the guild specified.",
                    "If `Start` is not given in the command, it will be",
                    "changed to `Stop`."
                ]
            },
            "install": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}plugin install",
                    "<Gist Plugin URL: String>"
                ],
                "info": [
                    "Downloads a plugin from the specified [URL]&",
                    "&(https://gist.github.com 'GistHub') and adds it to the",
                    "plugin directory of the bot, so that it can be added."
                ]
            },
            "delete": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}plugin delete",
                    "<File Name: String>"
                ],
                "info": [
                    "This deletes an entire plugin file from within the",
                    "`plugins` directory, some plugins cannot be deleted."
                ]
            },
            "add": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [],
                "info": []
            },
            "remove": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [],
                "info": []
            }
        },
        "guild": {
            "enable": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}guild enable",
                    "<Guild: Snowflake | 'self'>"
                ],
                "info": [
                    "Enables a guild to allow it's users to use the bot. If",
                    "`self` is given as second argument, it will enable the",
                    "guild that the command is being ran from."
                ]
            },
            "disable": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}guild disable",
                    "<Guild: Snowflake | 'self'>"
                ],
                "info": [
                    "Disables a guild to allow it's users to use the bot. If",
                    "`self` is given as second argument, it will disable the",
                    "guild that the command is being ran from."
                ]
            },
            "list": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}guild list",
                    "[Start: Integer]",
                    "[Stop: Integer]"
                ],
                "info": [
                    "Lists all guilds the bot is in and whether or not the",
                    "guild is enabled within the bot. If enabled, the guild",
                    "entry in the list will be green, if not enabled, it will",
                    "be red. If both arguments are not specified, `Start`",
                    "becomes the `Stop` argument."
                ]
            },
            "leave": {
                "DM_level": perm_ints["server_mod"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}guild leave",
                    "<Guild: Snowflake | 'Self'>"
                ],
                "info": [
                    "Has the bot leave a guild, if the guild is an admin",
                    "or emoji guild, it cannot be left through the use",
                    "of this command"
                ]
            }
        },
        "blacklist": {
            "add": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}blacklist add",
                    "<Type: 'Guild' | 'Channel' | 'User'>",
                    "<Entity: Mention | Snowflake>",
                    "[Reason...: String]"
                ],
                "info": [
                    "Adds the specified entity to the blacklist with the",
                    "given reason."
                ]
            },
            "remove": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}blacklist remove",
                    "<Type: 'Guild' | 'Channel' | 'User'>",
                    "<Entity: Mention | Snowflake>"
                ],
                "info": [
                    "Removes the entity from the specified blacklist."
                ]
            },
            "info": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}blacklist info",
                    "<Entity: Mention | Snowflake>",
                    "[Type: 'Guild' | 'Channel' | 'User']"
                ],
                "info": [
                    "Returns the information of the blacklisted entity, of",
                    "which includes, whom blacklisted it, when it was added",
                    "and the reason as to why it was blacklisted"
                ]
            },
            "list": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}blacklist list",
                    "<Type: 'Guild' | 'Channel' | 'User'>",
                    "[<Start: Integer>",
                    "<Stop: Integer>]"
                ],
                "info": [
                    "Displays a list of blacklisted entities within the given",
                    "blacklist type. To display certain ones, `Start` and",
                    "`Stop` must both be given otherwise the command will",
                    "error."
                ]
            },
            "reset": {
                "DM_level": perm_ints["global_admin"],
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "guild_level": perm_ints["global_admin"],
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}blacklist reset",
                    "[Type: 'Guild' | 'Channel' | 'User']"
                ],
                "info": [
                    "Resets the specified blacklist, if not given,",
                    "will reset all blacklists."
                ]
            }
        }
    }
    #=======================================#


#=============================================================================#
# COMMANDS:










#-----------------------------------------------------------------------------#
# PLUGIN COMMANDS:


    @Plugin.command("enable", group="plugin")
    def plugin_enable(self, event):



        # Argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = convert_guild_self(event.args[0], event.msg)
        plugin = event.args[1]


        # Ensure the plugin exists
        if plugin not in self.bot.plugins.keys():

            return event.msg.reply(
                GlobalAdmin.invalid_plugin.format(
                    plugin
                )
            )
        else:
            plugin = self.bot.plugins[plugin]

        # Ensure the plugin is allowed to be enabled
        if not plugin.can_be_enabled:
            return event.msg.reply(
                GlobalAdmin.cannot_be_enabled.format(
                    plugin
                )
            )

        config = PluginConfig.load("guild_list")

        # Plugin enabled already?
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


        # Argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = convert_guild_self(guild_id, event.msg)
        plugin = event.args[1]


        # Ensure the plugin exists
        if plugin not in self.bot.plugins:
            return event.msg.reply(
                GlobalAdmin.invalid_plugin.format(
                    plugin
                )
            )
        plugin = self.bot.plugins[plugin]


        # Ensure the plugin is enabled so we can disable it
        if not plugin.can_be_enabled:
            return event.msg.reply(
                GlobalAdmin.cannot_be_enabled.format(
                    plugin.name
                )
            )


        config = PluginConfig.load("guild_list")


        # Ensure guild is enabled
        if guild_id not in config:
            return event.msg.reply(
                GlobalAdmin.guild_not_enabled.format(guild_id)
            )


        # Plugin enabled?
        if plugin.name in config[guild_id]:

            config[guild_id].remove(plugin.name)
            event.msg.reply(
                GlobalAdmin.removed_plugin.format(
                    plugin.name,
                    guild_id
                )
            )

            # Update file
            PluginConfig.write("guild_list", config)

        else:

            # Acknowledge error
            event.msg.reply(
                GlobalAdmin.plugin_not_enabled.format(
                    plugin.name,
                    guild_id
                )
            )





    @Plugin.command("list", group="plugin")
    def plugin_list(self, event):


        # Ensure the user supplies at least one argument
        if len(event.args) < 1:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = convert_guild_self(event.args[0], event.msg)


        try:
            # Loading the guild's plugins
            enabled_plugins = PluginConfig.load("guild_list")[guild_id]
        except KeyError:
            return event.msg.reply(GlobalAdmin.invalid_arg.format(guild_id))


        # Convert arguments if given
        try:
            # End only
            if len(event.args) == 2:
                start = 0
                end = int(event.args[1])

            # Both
            elif len(event.args) == 3:
                start = int(event.args[1])
                end = int(event.args[2])

            # No arguments given
            else:
                start = 0
                end = len(self.bot.plugins)

        # Invalid integer given
        except ValueError:
            return event.msg.reply(GlobalAdmin.invalid_int)


        # Ensure start is not greater than end
        if (start - end) > 0:
            return event.msg.reply(GlobalAdmin.error)
        # Start == end (meaning no plugins to list)
        elif (start - end) == 0:
            return event.msg.reply(
                GlobalAdmin.no_list_zero.format(
                    "plugins"
                )
            )

        # Ensure user's "start" is lower than highest index
        if start > (len(self.bot.plugins) - 1):
            return event.msg.reply(
                GlobalAdmin.start_too_big.format(
                    len(self.bot.plugins) - 1
                )
            )

        response = GlobalAdmin.plugin_list.format(
            guild_id,
            filter_plugins(
                self.bot.plugins,
                enabled_plugins,
                start,
                end
            )
        )

        # Ensure message length
        if len(response) > 2000:
            return event.msg.reply(GlobalAdmin.message_too_long)

        # Acknowledge
        return event.msg.reply(response)





#-----------------------------------------------------------------------------#
# GUILD COMMANDS:


    @Plugin.command("enable", group="guild", aliases=["whitelist"])
    def guild_enable(self, event):


        guild_list = PluginConfig.load("guild_list")

        # Check if arguments used
        if len(event.args) < 1:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = convert_guild_self(event.args[0], event.msg)


        # Ensure guild not enabled
        if guild_id in guild_list.keys():
            return event.msg.reply(
                GlobalAdmin.guild_already_enabled.format(
                    guild_id
                )
            )

        # Add guild to file
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

        # Check if arguments used
        if len(event.args) < 1:
            return event.msg.reply(GlobalAdmin.nea)
        guild_id = convert_guild_self(event.args[0], event.msg)


        # Ensure guild not enabled
        if guild_id not in guild_list.keys():
            return event.msg.reply(
                GlobalAdmin.guild_not_enabled.format(
                    guild_id
                )
            )

        # Add guild to file
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


        # Convert arguments if given
        try:
            # End only
            if len(event.args) == 1:
                start = 0
                end = int(event.args[0])
            
            # Both
            elif len(event.args) == 2:
                start = int(event.args[0])
                end = int(event.args[1])

            # No arguments given
            else:
                start = 0
                end = len(self.state.guilds)

        # Invalid integer given
        except ValueError:
            return event.msg.reply(GlobalAdmin.invalid_int)


        # Ensure start is not greater than end
        if (start - end) > 0:
            return event.msg.reply(GlobalAdmin.error)

        # Start == end (meaning no guilds to list)
        elif (start - end) == 0:
            return event.msg.reply(
                GlobalAdmin.no_list_zero.format(
                    "guilds"
                )
            )


        # Ensure user's "start" is lower than highest index
        if start > (len(self.state.guilds) - 1):
            return event.msg.reply(
                GlobalAdmin.start_too_big.format(
                    len(self.state.guilds) - 1
                )
            )


        # Loading the guild list
        guild_list = PluginConfig.load("guild_list")


        guilds = []
        # Cycle through all guilds bot has loaded
        for guild in self.state.guilds:
            guild = self.state.guilds[guild]
            if str(guild.id) in guild_list:
                enabled = "+"
            else:
                enabled = "-"
            guilds.append(
                "{e} {g.name} ({g.id})".format(
                    e=enabled,
                    g=guild
                )
            )


        response = GlobalAdmin.guild_list.format(
            "\n".join(guilds[start:end])
        )


        # Ensure message length
        if len(response) > 2000:
            return event.msg.reply(GlobalAdmin.message_too_long)

        # Acknowledge
        event.msg.reply(response)





    @Plugin.command("leave", group="guild")
    def leave_guild(self, event):

        # Check for argument
        if event.args:

            # Ensure user is guild owner or admin
            if Perms.integer(event.msg.member) < perm_ints["global_admin"]:
                return event.msg.reply(GlobalAdmin.invalid_perms)

            guild_id = int(event.args[0])

            # Ensure guild ID in state
            if guild_id not in self.state.guilds:
                return event.msg.guild(
                    GlobalAdmin.invalid_arg.format(guild_id)
                )
            
            # Ensure guild isn't an admin guild:
            if guild_id not in Config.load()["admin"]["guilds"]:
                self.state.guilds[guild_id].leave()
            else:
                return event.msg.reply(GlobalAdmin.cannot_leave)
        
        else:

            # Ensure guild
            if not event.guild:
                return event.msg.reply(
                    GlobalAdmin.no_DMs
                )

            # Ensure user is guild owner or admin
            if Perms.integer(event.msg.member) < perm_ints["server_admin"]:
                return event.msg.reply(GlobalAdmin.invalid_perms)

            # Ensure guild isn't an admin guild:
            if event.guild.id not in Config.load()["admin"]["guilds"]:
                self.state.guilds[guild_id].leave()
            else:
                return event.msg.reply(GlobalAdmin.cannot_leave)





#-----------------------------------------------------------------------------#
# BLACKLIST COMMANDS:


    @Plugin.command("add", group="blacklist")
    def blacklist_add(self, event):
        
        # Argument checking
        if len(event.args) >= 3:
            blacklist_type = event.args[0].lower()
            entity = event.args[1].strip("<@!&#>")
            reason = " ".join(event.args[2:])

        # Not enough arguments error
        elif len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)

        # Bare minimum arguments given
        else:
            blacklist_type = event.args[0]
            entity = event.args[1].strip("<@!&#>")
            reason = None


        # Ensure valid blacklist type given
        if blacklist_type not in valid_blacklists:
            return event.msg.reply(
                GlobalAdmin.invalid_blacklist.format(blacklist_type)
            )


        #load blacklist
        data = Blacklist.load()


        # Ensure entity isn't already in specified blacklist
        if entity in data[blacklist_type]:
            return event.msg.reply(
                GlobalAdmin.entity_already_blacklisted.format(
                    entity,
                    blacklist_type
                )
            )


        # Add entity to blacklist
        getattr(Blacklist.Add, blacklist_type)(
            entity,
            event.msg.author.id,
            reason
        )

        return event.msg.reply(
            GlobalAdmin.blacklisted.format(
                entity,
                blacklist_type,
                reason
            )
        )



    @Plugin.command("remove", group="blacklist")
    def blacklist_remove(self, event):

        # Argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)
        blacklist_type = event.args[0]
        entity = event.args[1].strip("<@!&#>")


        # Ensure valid blacklist type given
        if blacklist_type not in valid_blacklists:
            return event.msg.reply(
                GlobalAdmin.invalid_blacklist.format(blacklist_type)
            )


        #load blacklist
        data = Blacklist.load()


        # Ensure entity isn't already in specified blacklist
        if entity not in data[blacklist_type]:
            return event.msg.reply(
                GlobalAdmin.entity_not_blacklisted.format(
                    entity,
                    blacklist_type
                )
            )


        # Remove entity from blacklist
        getattr(Blacklist.Remove, blacklist_type)(
            entity
        )

        return event.msg.reply(
            GlobalAdmin.unblacklisted.format(
                entity,
                blacklist_type
            )
        )



    @Plugin.command("info", group="blacklist")
    def blacklist_info(self, event):


        # Argument checking
        if len(event.args) < 2:
            return event.msg.reply(GlobalAdmin.nea)


        # Insantiate variables
        blacklist_type = event.args[0].lower()
        entity = event.args[1]


        # Ensure valid blacklist type given
        if blacklist_type not in valid_blacklists:
            return event.msg.reply(
                GlobalAdmin.invalid_blacklist.format(blacklist_type)
            )


        # Load blacklist
        data = Blacklist.load()

        # Ensure entity is blacklisted
        if entity not in data[blacklist_type]:
            return event.msg.reply(
                GlobalAdmin.entity_not_blacklisted.format(
                    entity,
                    blacklist_type
                )
            )


        # Get entity data
        data = Blacklist.get(blacklist_type, entity)

        return event.msg.reply(
            embed=BlacklistInfoEmbed(data)
        )