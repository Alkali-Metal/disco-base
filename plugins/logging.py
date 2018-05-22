"""
A plugin that automatically logs various events to a Discord channel specified
by the user.
"""
from data.types.bot.plugin_config import PluginConfig
from data.types.discord.embeds import LogEmbeds
from data.response import Logging, Invalid

from holster.emitter import Priority

from disco.types.message import MessageEmbed
from disco.bot import Plugin

import re


"""
GUILD_UPDATE = 1,
CHANNEL_CREATE = 10,
CHANNEL_UPDATE = 11,
CHANNEL_DELETE = 12,
CHANNEL_OVERWRITE_CREATE = 13,
CHANNEL_OVERWRITE_UPDATE = 14,
CHANNEL_OVERWRITE_DELETE = 15,
MEMBER_KICK = 20,
MEMBER_PRUNE = 21,
MEMBER_BAN_ADD = 22,
MEMBER_BAN_REMOVE = 23,
MEMBER_UPDATE = 24,
MEMBER_ROLE_UPDATE = 25,
ROLE_CREATE = 30,
ROLE_UPDATE = 31,
ROLE_DELETE = 32,
INVITE_CREATE = 40,
INVITE_UPDATE = 41,
INVITE_DELETE = 42,
WEBHOOK_CREATE = 50,
WEBHOOK_UPDATE = 51,
WEBHOOK_DELETE = 52,
EMOJI_CREATE = 60,
EMOJI_UPDATE = 61,
EMOJI_DELETE = 62,
MESSAGE_DELETE = 72
"""



regex = r"(https://(canary.discordapp|ptb.discordapp|discordapp)\.com/api/webhooks/(?P<ID>[0-9]{1,100})(?P<TOKEN>/?[A-Za-z-0-9]*))|(?P<ID_ONLY>[0-9]{1,100})"

valid_events = [
    "GUILD_AVAILABLE",
    "GUILD_UNAVAILABLE",
    "CHANNEL_CREATE",
    "CHANNEL_UPDATE",
    "CHANNEL_DELETE",
    "MESSAGE_DELETE"
]



def is_enabled(event):

    # Check typing of argument given
    if (type(event) == type(1)) or (type(event) == type("")):
        guild_id = str(event)
    else:
        guild_id = str(event.guild.id)

    # Load the guid list
    guild_list = PluginConfig.load("guild_list.json")

    # Ensure guild is enabled
    if guild_id in guild_list:

        # Ensure plugin is enabled in guild
        if "GuildLogging" in guild_list[guild_id]:

            return True
    return False



def webhook_fetch(self, event, log_event):

    webhook_list = []
    guild_id = str(event.guild.id)


    # Load configuration
    data = PluginConfig.load("logger.json")

    # Filter through webhooks to see if there are any with the event so
    #  we don't end up spamming the API with GET requests for webhooks
    #  we aren't even pushing anything to.
    if log_event != "GET_ALL_WEBHOOKS":
        for webhook in data[guild_id]:
            if log_event in data[guild_id][webhook]["list"]:
                webhook_list.append(webhook)
        if len(webhook_list) == 0:
            return []
        webhook_list = []


    try:
        #Get list of guild webhooks
        webhooks = self.bot.client.api.guilds_webhooks_list(event.guild.id)
    except:
        return


    # See if we are just getting a list of all webhooks
    if log_event == "GET_ALL_WEBHOOKS":

        # Cycle through webhooks
        for webhook in webhooks:
            webhook_list.append(str(webhook.id))
        return webhook_list


    # Cycle through webhooks to see which to trigger
    for webhook in webhooks:

        # Check if the webhook is that of the bot's
        if str(webhook.id) in data[guild_id]:

            # Check if the event is in the desired webhook's log list
            if log_event in data[guild_id][str(webhook.id)]["list"]:
                webhook_list.append(webhook)

    return webhook_list



def get_response(event, webhook, log_event):

    # Load configuration
    data = PluginConfig.load("logger.json")

    # Grab log type
    log_type = data[str(event.guild.id)][str(webhook.id)]["options"]["type"]


    # ---------- Check log type and create response accordingly

    #Log type: rich (embeded)
    if log_type == "rich":
        if hasattr(LogEmbeds, log_event):
            return [None, getattr(LogEmbeds, log_event)(event)]
        else:
            raise NameError(
                "LogEmbeds doesn't have attribute `{}`".format(log_event)
            )

    # Log type: moderate (non-embeded, but with more than one line)
    elif log_type == "moderate":

        # Ensure that there is a function for the event
        if hasattr(Logging.moderate, log_event):
            # Return the string from the function
            return [getattr(Logging.moderate, log_event)(event)]
        else:
            raise NameError(
                "Logging.moderate doesn't have attribute `{}`".format(
                    log_event
                )
            )

    # Log type: compact (non-embeded, try to keep to one line on desktop views)
    elif log_type == "compact":

        # Ensure that there is a function for the event
        if hasattr(Logging.compact, log_event):
            # Return the string from the function
            return [getattr(Logging.compact, log_event)(event)]
        else:
            raise NameError(
                "Logging.compact doesn't have attribute `{}`".format(log_event)
            )



def webhook_url_check(event, webhook):

    match = re.match(regex, webhook)

    # See if the user gave us a URL argument
    if match:

        # Check to see which argument type they gave
        if match.group("ID"):

            # Try to remove the message if the user sent the token to the chat
            if match.group("TOKEN"):
                try:
                    event.msg.delete()
                except:
                    event.msg.reply(Logging.message_delete_error)
            return [True, match.group("ID")]

        elif match.group("ID_ONLY"):
            return [True, match.group("ID_ONLY")]

    else:
        # Try to remove the message if the user sent the token to the chat
        if len(webhook.split("/")) >= 7:
            try:
                event.msg.delete()
            except:
                event.msg.reply(Logging.message_delete_error)
        event.msg.reply(Invalid.argument.format("<Webhook ID | Webhook URL>"))
        return [False, None]









class GuildLogging(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 2.0
    config_settings = None
    plugin_info = []
    commands_config = {
        "log": {
            "add": {
                "allow_DMs": False,
                "bot_perms": 536870912,
                "user_perms": 0,
                "default_level": 1,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            },
            "remove": {
                "allow_DMs": False,
                "bot_perms": 536870912,
                "user_perms": 0,
                "default_level": 1,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            },
            "event add": {
                "allow_DMs": False,
                "bot_perms": 0,
                "user_perms": 16,
                "default_level": 1,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            }
        }
    }
    #=======================================#


#=============================================================================#
# COMMANDS



    @Plugin.command("add", group="log")
    def log_add(self, event):


        # Argument checking
        if len(event.args) == 1:
            webhook = event.args[0]
            log_type = "rich"
        elif len(event.args) == 2:
            webhook = event.args[0]
            log_type = event.args[1].lower
        else:
            return event.msg.reply(Logging.nea)


        guild_id = str(event.guild.id)


        webhook_valid, webhook_id = webhook_url_check(event, webhook)


        # Ensure webhook is valid
        if not webhook_valid:
            return


        # Get all webhooks then ensure that permissions are valid
        webhooks = webhook_fetch(self, event, "GET_ALL_WEBHOOKS")
        if not webhooks:
            return


        # Ensure the user gave us a valid webhook ID/URL
        if webhook_id not in webhooks:
            return event.msg.reply(Logging.invalid_webhook)


        # Ensure log type is a valid type
        if log_type not in ("rich", "compact", "moderate"):
            return event.msg.reply(Logging.invalid_log_type.format(log_type))


        # Add log webhook to configuration
        data = PluginConfig.load("logger.json")
        if guild_id in data:

            # Ensure webhook isn't already a log
            if webhook_id not in data[guild_id]:
                data[guild_id][webhook_id] = {
                    "options": {
                        "type": log_type
                    },
                    "list": []
                }
                PluginConfig.write("logger.json", data)
                return event.msg.reply(Logging.webhook_added.format(
                    webhook_id,
                    event.args[1])
                )
            return event.msg.reply(Logging.already_log.format(webhook_id))
        else:
            return event.msg.reply(Logging.guild_not_setup)



    @Plugin.command("remove", group="log")
    def log_remove(self, event):

        # Argument checking
        if len(event.args) < 1:
            return event.msg.reply(Logging.nea)
        else:
            webhook = event.args[0]


        guild_id = str(event.guild.id)


        webhook_valid, webhook_id = webhook_url_check(event, webhook)


        # Ensure webhook is valid
        if not webhook_valid:
            return


        # Add log webhook to configuration
        data = PluginConfig.load("logger.json")
        if guild_id in data:

            # Ensure webhook isn't already a log
            if webhook_id in data[guild_id]:
                data[guild_id].pop(webhook_id)
                PluginConfig.write("logger.json", data)
                return event.msg.reply(Logging.webhook_removed.format(
                    webhook_id)
                )
            return event.msg.reply(Logging.not_log.format(webhook_id))
        else:
            return event.msg.reply(Logging.guild_not_setup)



    #@Plugin.command("create", group="log")
    def log_create(self, event):
        pass



    @Plugin.command("event add", group="log")
    def event_add(self, event):

        # Argument checking
        if len(event.args) < 2:
            return event.msg.reply(Logging.nea)


        # Variable declarations
        events = event.args[1:]
        guild_id = str(event.msg.guild.id)
        webhook_valid, webhook_id = webhook_url_check(event, event.args[0])


        # Ensure webhook is valid
        if not webhook_valid:
            return

        # Ensure the user gave us a valid webhook ID/URL
        if webhook_id not in webhook_fetch(self, event, "GET_ALL_WEBHOOKS"):
            return event.msg.reply(Logging.invalid_webhook)

        added = []
        invalid = []

        # Load config data
        data = PluginConfig.load("logger.json")

        # Cycle through events given and construct response lists
        for log_event in events:
            log_event = log_event.upper()

            # Valid log event
            if log_event in valid_events:
                added.append(log_event)
                data[guild_id][webhook_id]["list"].append(log_event)

            # Invalid log event
            else:
                invalid.append(log_event)
        
        # Create response
        response = Logging.event_base_response


#=============================================================================#
# BASE EVENT HANDLER
#   What the main event listeners use to execute their main event handlings,
#   any additional checks required are done within the actual listner itself

    def base_event_handler(self, event, bot_event):

        # Get a list of webhooks that have the event enabled
        webhooks = webhook_fetch(self, event, bot_event)

        # Ensure that we didn't error
        if webhooks == None:
            return

        # Cycle through webhooks pushing to them
        for webhook in webhooks:

            #Get the webhook response
            response = get_response(event, webhook, bot_event)

            # Ensure embeds are supplied if needed
            if len(response) > 1:
                # HEEEEEEEAAAAAVEEEEEEEE
                webhook.execute(content=response[0], embeds=response[1:])
            else:
                webhook.execute(content=response[0])


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# GUILD EVENTS


    # Guild Available Event (Extension)
    @Plugin.listen("GuildCreate", conditional=is_enabled)
    def message_delete(self, event):

        # Ensure the guild is available and it isn't a guild being joined
        if event.created:
            return

        self.base_event_handler(event, "GUILD_AVAILABLE")


    # Guild Unavailable Event (Extension)
    @Plugin.listen("GuildDelete", conditional=is_enabled)
    def message_delete(self, event):

        # Ensure the guild is unavailable and not being deleted
        if event.deleted:
            return

        self.base_event_handler(event, "GUILD_UNAVAILABLE")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# CHANNEL EVENTS


    @Plugin.listen("ChannelCreate", conditional=is_enabled)
    def channel_add(self, event):
        self.base_event_handler(event, "CHANNEL_CREATE")


    @Plugin.listen("ChannelUpdate", conditional=is_enabled)
    def channel_update(self, event):
        self.base_event_handler(event, "CHANNEL_UPDATE")


    @Plugin.listen("ChannelDelete", conditional=is_enabled)
    def channel_delete(self, event):
        self.base_event_handler(event, "CHANNEL_DELETE")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# MESSAGE EVENTS


    @Plugin.listen("MessageDelete", conditional=is_enabled)
    def message_delete(self, event):
        self.base_event_handler(event, "MESSAGE_DELETE")


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ROLE EVENTS


    @Plugin.listen("GuildRoleCreate", conditional=is_enabled)
    def role_create(self, event):
        self.base_event_handler(event, "ROLE_CREATE")