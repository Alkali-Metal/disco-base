# BOT IMPORTS:
from data.types.discord.permissions import Bot, User, Misc
from data.response import Parser, Invalid, GlobalAdmin
from data.types.bot.plugin_config import PluginConfig
from data.types.bot.guild_config import GuildConfig
from data.types.bot.blacklist import Blacklist
from data.types.bot.permissions import Perms
from data.types.bot.config import Config

# DISCO IMPORTS:
from disco.bot import Plugin

# MISC MODULE IMPORTS:
from time import sleep



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

    # Ensure the message starts with the prefix
    if event.message.content.startswith(prefix):

        # See if we are needing mentions for commands
        require_mention = config["bot"]["commands_require_mention"]
        
        # See if the user supplied command mention rules
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





class MessageParser(Plugin):


    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = False
    can_reload = False
    restricted = False
    force_default = True
    bypass_enabled = True
    can_be_enabled = False
    plugin_version = 4.1
    config_settings = None
    plugin_info = [
        "The message parser for the bot. This plugin cannot be enabled and",
        "has no functionality other than MAKING THE ENTIRE BOT WORK.",
        "So this plugin cannot be enabled nor disabled. TAKE THAT MOM!"
    ]
    commands_config = {
        "bot": {
            "reload": {
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 4,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}bot reload",
                    "<Plugins...: string>"
                ],
                "info": [
                    "Reloads plugins from the specified list. Not all plugins",
                    "can actually be reloaded. If they cannot be reloaded,",
                    "the bot will alert you of this in the response."
                ]
            }
        }
    }
    #=======================================#


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

            # Ensure that config allows edited message commands
            if config["bot"]["commands_allow_edit"]:

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

                # Ensure message startswith the prefix
                if event.message.content.startswith(prefix):

                    # See if we're responding to invalid
                    if config["parser"]["respond_to_invalid"]:

                        # Ensure we can send messages
                        if event.channel.get_permissions(
                            self.state.me
                        ).can(2048):
                            return event.message.reply(Invalid.command)


                        # if we can't send messages check if we can add reactions
                        elif event.channel.get_permissions(
                            self.state.me
                        ).can(262208):
                            return event.message.add_reaction(
                                custom_emojis["red_tick"]
                            )

                        else:
                            return
                    else:
                        return
                else:
                    return


            #-----------------------------------------------------------------#
            # Erroring if we don't have the absolute bare minimum permissions
            #  for anything, (ie: sending messages)

            # Ensure we have send message permissions, else, error
            if not event.channel.get_permissions(
                self.state.me
            ).can(2048):
                return


            #-----------------------------------------------------------------#
            # Parsing message if it has a command trigger


            # commands are indeed triggered:
            command = commands[0][0]
            plugin = command.plugin

            try:
                cmd_config = plugin.commands_config[str(command.group)][command.name]
                allow_DMs = cmd_config["allow_DMs"]
                bot_perms = cmd_config["bot_perms"]
                user_perms = cmd_config["user_perms"]
                default_level = cmd_config["default_level"]
            except:
                return event.message.reply(Parser.generic_error)


            #-----------------------------------------------------------------#
            # Ensure that we are not attempting to run an indev plugin from a
            #  production bot.

            # Ensure environment is production, in dev we want to allow all
            if config["do_not_change"]["env"] == "prod":

                # Ensure plugin is not in dev
                if plugin.in_dev:

                    # Ensure guild is not allowing development plugins
                    if GuildConfig.load(event.message.guild.id)["allow_dev"]:
                        return event.message.reply(
                            Parser.plugin_in_dev
                        )


            #-----------------------------------------------------------------#
            # Ensure that we have a guild to work with for permissions,
            #  otherwise use defaults for DMs and ensure command is enabled
            #  in DMs


            # message in guild
            if guild:

                guild_list = PluginConfig.load("guild_list")


                #-------------------------------------------------------------#
                # Plugin doesn't need to be enabled then ensure that the guild
                #  is enabled with the plugin enabled, otherwise error
                #  accordingly.


                # Check if plugin bypasses the enabled checks.
                if not plugin.bypass_enabled:


                    # ensure guild is enabled
                    if str(guild.id) not in guild_list:
                        return event.message.reply(Parser.guild_not_enabled)


                    # ensure guild has the plugin enabled
                    if plugin.name not in guild_list[str(guild.id)]:
                        return event.message.reply(
                            Parser.not_plugin_enabled.format(plugin.name)
                        )


                #-------------------------------------------------------------#
                # Ensure that the plugin isn't restricted and that the guild
                #  can is also not restricted if the plugin is

                # load guild's configuration
                config = GuildConfig.load(event.message.guild.id)

                # Check if the plugin and guild are restricted then deny if so
                if (config["restricted"] and plugin.restricted):
                    return event.message.reply(Parser.restricted)



                #-------------------------------------------------------------#
                # Ensure that the plugin isn't one where we force the default
                #  configuration on otherwise try to load the guild config,
                #  and if something goes wrong with the guild config, resort
                #  to the default config.

                # Check if we're forcing default
                if not plugin.force_default:

                    # get command permission level
                    try:


                        plg_data = config["cmd_lvls"][plugin.name]


                        # command with group
                        if command.group:
                            cmd_level = plg_data[command.group][command.name]
                            


                        # command no group
                        else:

                            cmd_level = plg_data[command.name]
                            bypass_user_perms = config["permissions"]["bypass_user_perms"]


                    # something went wrong, resort to default config
                    except KeyError:
                        cmd_level = default_level
                        bypass_user_perms = cmd_config["bypass_user_perms"]


                # Loading the default config file
                else:
                    cmd_level = default_level
                    bypass_user_perms = cmd_config["bypass_user_perms"]


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

                # Ensure we aren't ignoring user_perms
                if not bypass_user_perms:

                    # Ensure user has full permissions
                    if not event.message.channel.get_permissions(
                        event.message.member
                    ).can(user_perms):

                        # Ensure there is a command group
                        if command.group:
                            cmd = command.group + " " + command.name
                        else:
                            cmd = command.name

                        return event.msg.reply(
                            Parser.bot_perm_missing.format(
                                Config["bot"]["commands_prefix"],
                                cmd
                            )
                        )


                # Ensure bot has all permissions needed
                if not event.message.channel.get_permissions(
                    self.state.me
                ).can(bot_perms):

                    # Ensure there is a command group
                    if command.group:
                        cmd = command.group + " " + command.name
                    else:
                       cmd = command.name

                    return event.msg.reply(
                        Parser.bot_perm_missing.format(
                            Config["bot"]["commands_prefix"],
                            cmd
                        )
                    )


            # command ran in DMs
            elif allow_DMs:

                # Ensure we aren't ignoring user_perms
                if not bypass_user_perms:

                    # Ensure user has full permissions
                    if not event.message.channel.get_permissions(
                        event.message.member
                    ).can(user_perms):

                        # Ensure there is a command group
                        if command.group:
                            cmd = command.group + " " + command.name
                        else:
                            cmd = command.name

                        return event.msg.reply(
                            Parser.bot_perm_missing.format(
                                Config["bot"]["commands_prefix"],
                                cmd
                            )
                        )


                # Ensure bot has all permissions needed
                if not event.message.channel.get_permissions(
                    self.state.me
                ).can(bot_perms):

                    # Ensure there is a command group
                    if command.group:
                        cmd = command.group + " " + command.name
                    else:
                       cmd = command.name


                    return event.msg.reply(
                        Parser.bot_perm_missing.format(
                            Config["bot"]["commands_prefix"],
                            cmd
                        )
                    )

            # not allowing direct message commands
            else:
                return event.message.reply(Parser.not_DM_enabled)


            # handle message
            self.bot.handle_message(event.message)





#=============================================================================#
# ACTUAL EVENT LISTENERS:

    # Message Created
    @Plugin.listen("MessageCreate")
    def on_message_create(self, event):
        # try:
        self.message_handling(event, False)
        # except:
            # pass


    # Message Edited
    @Plugin.listen("MessageUpdate")
    def on_message_update(self, event):
        #try:
        self.message_handling(event, True)
        #except:
            # pass



#=============================================================================#



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
                if plugin.can_reload:
                    reloaded_plugins.append(plugin)
                    plugins[plugin].reload()

                # Didn't reload because we can't
                else:
                    didnt_reload.append(plugin)


        # reloading only certain plugins
        else:

            # filter through arguments given
            for plugin in event.args:

                # ensure valid plugin
                if plugin in plugins.keys():

                    # check if we can't reload the plugin
                    if not plugins[plugin].can_reload:
                        cannot_reload.append(plugin)
                        continue

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

        # Ensure response isn't too long.
        if 2000 > len(response) > 0:
            event.msg.reply(response)

        # Error in the chat
        else:
            event.msg.reply(GlobalAdmin.reload_too_long)