from data.types.discord.permissions import Bot, User, Misc
from data.response import Parser, Invalid, GlobalAdmin
from data.types.bot.plugin_config import PluginConfig
from data.types.bot.guild_config import GuildConfig
from data.types.bot.blacklist import Blacklist
from data.types.bot.permissions import Perms
from data.types.bot.config import Config

from disco.bot import Plugin

from time import sleep



enabled_bypass = [
    "GlobalAdministration",
    "ReloadCommand",
    "ConfigEditor"
]

force_default = [
    "GlobalAdministration",
    "ReloadCommand"
]

cannot_be_enabled = [
    "GlobalAdministration",
    "MessageParser",
    "AdminLogging",
    "ReloadCommand",
    "ConfigEditor"
]

cannot_reload = [
    "ReloadCommand",
    "MessageParser"
]



def is_blacklisted(event):
    blacklist = Blacklist.load()

    # user
    if event.message.author.id in blacklist["users"]:
        return True
    # channel
    elif event.message.channel in blacklist["channels"]:
        return True
    # guild
    elif event.guild:
        if event.message.guild.id in blacklist["guilds"]:
            return True
    return False



def triggers_commands(self, event):
    config = Config.load()

    prefix = config["bot"]["commands_prefix"]
    if event.message.content.startswith(prefix):
        require_mention = config["bot"]["commands_require_mention"]
        try:
            mention_rules = config["bot"]["commands_mention_rules"]
        except KeyError:
            mention_rules = {}

        # Get the commands that the message activates
        commands = self.bot.get_commands_for_message(
            require_mention,
            mention_rules,
            prefix,
            event.message   # TODO: Fix bug: https://trello.com/c/4AvBhOZf
        )

        # Ensure the activated commands count != 0
        if len(commands):
            return commands
        return
    return



def check_permissions(APIClient, event, permissions):

    # BOT PERMISSIONS
    if len(permissions["bot"]):

        # Ensure the bot has full permissions needed
        for permission in permissions["bot"]:

            # Ensure bot actually has permission
            bot_perms = event.message.guild.get_member()
            if Bot.has_perm(APIClient, event.message.guild, permission):
                continue
            else:

                # Acknowledge user then prevent further action
                event.message.reply(
                    Parser.bot_perm_missing.format(
                        Misc.convert(permission)
                    )
                )
                return False
    

    # USER PERMISSIONS
    if len(permissions["user"]):

        # Ensure the user has full permissions
        for permission in permissions["user"]:

            # Ensure user actually has the permission
            if User.has_perm(event.member, permission):
                continue
            else:

                # Acknowledge user then prevent further action
                event.message.reply(
                    Parser.user_perm_missing.format(
                        Misc.convert(permission)
                    )
                )
                return False
    
    # It's made it this far, we should probably allow it to actually continue
    return True




class MessageParser(Plugin):


    def message_handling(self, event, is_edited=False):
        
        config = Config.load()



#=============================================================================#
# MISC CHECKS


        # ensure only the custom parser is enabled
        if not config["bot"]["commands_enabled"]:


            # Ignore bots
            if event.message.author.bot:
                return


            # blacklist enabled?
            if config["parser"]["blacklist_enabled"]:
                if is_blacklisted(event):
                    return


            # ensure guild
            guild = None
            if event.message.guild != None:
                guild = event.message.guild


            # ensure message object content isn't unset
            if not hasattr(event.message.content, "startswith"):
                return

#=============================================================================#
# EDITED MESSAGE CHECKS


            # Ensure that we are checking an edited message
            if is_edited:

                # Ensure message is the most recent in channel
                msg_list = self.client.api.channels_messages_list(
                    event.message.channel_id,
                    limit=1
                )

                # Ensure message is most recent
                if msg_list[0].id != event.message.id:
                    return


#=============================================================================#
# BASIC COMMAND PARSING


            #-----------------------------------------------------------------#
            # No command responses


            # Get list of commands triggered
            commands = triggers_commands(self, event)


            # No commands triggered
            if commands == None:

                prefix = config["bot"]["commands_prefix"]

            #-----------------------------------------------------------------#

                # ensure message startswith the prefix
                if event.message.content.startswith(prefix):

                #-------------------------------------------------------------#

                    # see if we're responding to invalid
                    if config["parser"]["respond_to_invalid"]:
                        return event.message.reply(Invalid.command)
                    else:
                        return
                else:
                    return


            #-----------------------------------------------------------------#
            # Parsing message if it has a command trigger


            # commands are indeed triggered:
            cmd_name = commands[0][0].name
            cmd_group = commands[0][0].group
            plg_name = commands[0][0].plugin.name


            # Load the data that we will need for the command checking
            reqs = PluginConfig.load("command_requirements")


            #-----------------------------------------------------------------#
            # Ensure that we have a guild to work with for permissions,
            #  otherwise use defaults for DMs and ensure command is enabled
            #  in DMs


            # message in guild
            if guild != None:

                guild_list = PluginConfig.load("guild_list")


                #-------------------------------------------------------------#
                # Plugin doesn't need to be enabled then ensure that the guild
                #  is enabled with the plugin enabled, otherwise error
                #  accordingly.


                # Check if plugin bypasses the enabled checks.
                if plg_name not in enabled_bypass:


                    # ensure guild is enabled
                    if str(guild.id) not in guild_list:
                        return event.message.reply(Parser.guild_not_enabled)


                    # ensure guild has the plugin enabled
                    if plg_name not in guild_list[str(guild.id)]:
                        return event.message.reply(
                            Parser.not_plugin_enabled.format(plg_name)
                        )


                #-------------------------------------------------------------#
                # Ensure that the plugin isn't one where we force the default
                #  configuration on otherwise try to load the guild config,
                #  and if something goes wrong with the guild config, resort
                #  to the default config.

                # Check if we're forcing default
                if plg_name not in force_default:

                    # get command permission level
                    try:
                        # load guild's configuration
                        config = GuildConfig.load(event.message.guild.id)

                        # command with group
                        if cmd_group != None:
                            grp_data = config["cmd lvls"][plg_name][cmd_group]
                            cmd_level = grp_data[cmd_name]

                        # command no group
                        else:
                            cmd_level = config["cmd lvls"][plg_name][cmd_name]


                    # guild hasn't changed the permission level from default
                    except KeyError:
                        config = GuildConfig.load("default")

                        # command with group
                        if cmd_group != None:
                            grp_data = config["cmd lvls"][plg_name][cmd_group]
                            cmd_level = grp_data[cmd_name]

                        # command no group
                        else:
                            cmd_level = config["cmd lvls"][plg_name][cmd_name]

                # Loading the default config file
                else:
                    config = GuildConfig.load("default")

                    # command with group
                    if cmd_group != None:
                        grp_data = config["cmd lvls"][plg_name][cmd_group]
                        cmd_level = grp_data[cmd_name]
                    # command no group
                    else:
                        cmd_level = config["cmd lvls"][plg_name][cmd_name]


                #-------------------------------------------------------------#
                # Ensure user has the proper permission level to run the
                #  command and return an invalid permissions response if they
                #  do not.

                user_level = Perms.integer(event.message.member)
                if user_level < cmd_level:
                    return event.message.reply(Invalid.permissions)


                #-------------------------------------------------------------#
                # Checking to see if the bot/user have all the mandatory
                #  permissions


                # check to see if the command has a group
                if cmd_group != None:


                    # Get boolean value of whether or not they have permissions
                    has_permissions = check_permissions(
                        self.client.api,
                        event,
                        reqs[plg_name][cmd_group][cmd_name]
                    )


                    # Error if they don't have the valid permissions
                    if not has_permissions:
                        return


                # command has no group
                else:

                    # Get boolean value of whether or not they have permissions
                    has_permissions = check_permissions(
                        self.client.api,
                        event,
                        reqs[plg_name][cmd_name]
                    )


                    # Error if they don't have the valid permissions
                    if not has_permissions:
                        return


            # command ran in DMs
            else:


                # ensure command group
                if cmd_group != None:


                    # ensure that command has DMs enabled
                    if not reqs[plg_name][cmd_group][cmd_name]["DMs"]:
                        return event.message.reply(Parser.not_DM_enabled)


                    # Get boolean value of whether or not they have permissions
                    has_permissions = check_permissions(
                        self.client.api,
                        event,
                        reqs[plg_name][cmd_group][cmd_name]
                    )


                    # Error if they don't have the valid permissions
                    if not has_permissions:
                        return


                # command no group
                else:

                    # ensure that command has DMs enabled
                    if not reqs[plg_name][cmd_name]["DMs"]:
                        return event.message.reply(Parser.not_DM_enabled)


                    # Get boolean value of whether or not they have permissions
                    has_permissions = check_permissions(
                        self.client.api,
                        event,
                        reqs[plg_name][cmd_group][cmd_name]
                    )


                    # Error if they don't have the valid permissions
                    if not has_permissions:
                        return


            # handle message
            self.bot.handle_message(event.message)





#=============================================================================#
# ACTUAL EVENT LISTENERS:

    # Message Created
    @Plugin.listen("MessageCreate")
    def on_message_create(self, event):
        self.message_handling(event)

    # Message Edited
    @Plugin.listen("MessageUpdate")
    def on_message_update(self, event):
        self.message_handling(event, True)



#=============================================================================#



class ReloadCommand(Plugin):
    @Plugin.command("reload", group="bot")
    def reload_plugins(self, event):

        # argument checking
        if not len(event.args):
            return event.msg.reply(GlobalAdmin.nea)

        # get plugins
        plugins = self.bot.plugins
        reloaded_plugins = []
        invalid_plugins = []
        didnt_reload = []


        # reloading all plugins
        if event.args[0].lower() == "all":

            # cycle through plugins reloading them
            for plugin in plugins:

                # Ensure plugin can be reloaded
                if plugin not in cannot_reload:
                    reloaded_plugins.append(plugin)
                    plugins[plugin].reload()
                else:
                    didnt_reload.append(plugin)


        # reloading only certain plugins
        else:

            # filter through arguments given
            for plugin in event.args:

                # Ensure the plugin can be reloaded.
                if plugin in cannot_reload:
                    didnt_reload.append(plugin)
                    continue

                # ensure valid plugin
                if plugin in plugins.keys():
                    plugins[plugin].reload()
                    reloaded_plugins.append(plugin)

                # add to invalid list
                else:
                    invalid_plugins.append(plugin)


        # Create response text
        response = ""

        # Check for reloaded plugins
        if len(reloaded_plugins):
            response = GlobalAdmin.reloaded_plugins.format(
                ", ".join(
                    reloaded_plugins
                )
            )

        # Check for invalid plugins
        if len(invalid_plugins):
            response = response + "\n\n" + GlobalAdmin.invalid_plugins.format(
                ", ".join(invalid_plugins)
            )
        
        # Check for plugins we couldn't reload
        if len(didnt_reload):
            response = response + "\n\n" + GlobalAdmin.didnt_reload_plugins.format(
                ", ".join(didnt_reload)
            )

        if 2000 > len(response) > 0:
            event.msg.reply(response)