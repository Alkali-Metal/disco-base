# BOT IMPORTS:
from data.response import Admin

# DISCO IMPORTS:
from disco.bot import Plugin

# MISC MODULE IMPORTS:
from time import sleep



class Administration(Plugin):


    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = True
    can_reload = True
    restricted = False
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 1.0
    config_settings = None
    plugin_info = [
        "Provides useful commands for administrators and moderators."
    ]
    commands_config = {
        "None": {
            "ban": {
                "allow_DMs": False,
                "bot_perms": 2052,
                "user_perms": 4,
                "default_level": 1,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}ban",
                    "<User: user mention>",
                    "[Reason...: string]"
                ],
                "info": [
                    "Bans a user with the given reason, reason not mandatory."
                ]
            },
            "forceban": {
                "allow_DMs": False,
                "bot_perms": 2052,
                "user_perms": 4,
                "default_level": 1,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}forceban",
                    "<User: user ID>",
                    "[Reason...: string]"
                ],
                "info": [
                    "Bans the user with the specified ID, reason is not",
                    "mandatory, used if given."
                ]
            },
            "massban-reason": {
                "allow_DMs": False,
                "bot_perms": 2052,
                "user_perms": 4,
                "default_level": 2,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}massban-reason",
                    "[--<ID: string>=<Reason...>]..."
                ],
                "info": [
                    "Allows banning a large amount of users by ID, reasons",
                    "are not supported with this command."
                ]
            },
            "massban": {
                "allow_DMs": False,
                "bot_perms": 2052,
                "user_perms": 4,
                "default_level": 2,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}massban",
                    "[--<ID: string>=<Reason...>]..."
                ],
                "info": [
                    "Allows banning a large amount of users by ID, with an",
                    "individual reason for each user"
                ]
            }
        },
        "clean": {
            "channel": {
                "allow_DMs": False,
                "bot_perms": 76800,
                "user_perms": 8192,
                "default_level": 3,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}clean channel",
                    "[Amount: integer]"
                ],
                "info": [
                    "Cleans a channel of `[Amount]` messages, this will not",
                    "delete a message if it is pinned in the channel. If",
                    "`[Amount]`"
                ]
            },
            "bot": {
                "allow_DMs": True,
                "bot_perms": 68608,
                "user_perms": 8192,
                "default_level": 0,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}clean bot",
                    "[Amount: integer]"
                ],
                "info": [
                    "Cleans a channel of `[Amount]` messages that this bot",
                    "has sent. If `[amount]` is unspecified it will clean all."
                ]
            },
            "user": {
                "allow_DMs": False,
                "bot_perms": 68608,
                "user_perms": 8192,
                "default_level": 1,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}clean user",
                    "<User: snowflake | user mention>",
                    "[Amount: integer]"
                ],
                "info": [
                    "Cleans a channel of `[Amount]` messages that this bot",
                    "has sent. If `[amount]` is unspecified it will clean all."
                ]
            }
        }
    }
    #=======================================#



#=============================================================================#
# COMMANDS:

    @Plugin.command("ban")
    @Plugin.command("forceban")
    def ban_user(self, event):

        # Argument checking
        if len(event.args) == 0:
            return event.msg.reply(Admin.nea)


        try:
            target = int(event.args[0].strip("<@!>"))
        except:
            target = event.guild.get_member(event.args[0]).id


        if len(event.args) >= 2:
            reason = " ".join(event.args[1:])

        # Ensure user isn't trying to ban themselves
        if target == event.msg.author.id:
            return event.msg.reply(Admin.no_ban_self)

        # Ensure not already banned
        if target in event.msg.guild.get_bans().keys():
            return event.msg.reply(Admin.already_banned)

        # Banning
        event.msg.guild.create_ban(target, reason=reason)
        
        user = event.msg.guild.get_bans()[target].user

        # Acknowledge
        event.msg.reply(
            Admin.ban_success.format(
                user.username,
                user.id,
                reason
            )
        )



    @Plugin.command("massban-reason")
    def reason_massban(self, event):

        # Argument checking
        if not len(event.args):
            return event.msg.reply(Admin.nea)

        args = " ".join(event.args).split("--")
        users_to_ban = {}


        # Cycle through each of the given users and add to the dict
        for arg in args:

            # Ensure the string is not just empty
            if len(arg):
                # Ensure the argument is valid
                if "=" in arg:
                    ID, reason = arg.split("=")

                    # Ensure user isn't trying to ban themselves
                    if int(ID) != event.msg.author.id:
                        users_to_ban[ID] = reason

        already_banned_users = 0
        banned_users = 0
        GUILD_BAN_LIST = event.msg.guild.get_bans().keys()


        # Cycle through banning each user
        for user in users_to_ban:

            target = user
            reason = users_to_ban[user]

            # Ensure not already banned
            if int(target) in GUILD_BAN_LIST:
                already_banned_users += 1
                continue

            # Banning
            event.msg.guild.create_ban(
                target,
                reason=reason
            )
            banned_users += 1
            sleep(2)


        # Acknowledge
        event.msg.reply(
            Admin.mass_ban.format(
                len(users_to_ban),
                banned_users,
                already_banned_users
            )
        )



    @Plugin.command("massban")
    def massban(self, event):

        # Argument checking
        if not len(event.args):
            return event.msg.reply(Admin.nea)

        args = " ".join(event.args).split("--")


        # Cycle through each of the given users and add to the dict
        for arg in args:

            # Ensure the string is not just empty
            if len(arg):
                # Ensure the argument is valid
                if "=" in arg:
                    ID, reason = arg.split("=")

                    # Ensure user isn't trying to ban themselves
                    if int(ID) != event.msg.author.id:
                        users_to_ban[ID] = reason


        already_banned_users = 0
        banned_users = 0
        GUILD_BAN_LIST = event.msg.guild.get_bans().keys()

        # Cycle through banning each user
        for user in users_to_ban:

            target = user

            # Ensure not already banned
            if int(target) in GUILD_BAN_LIST:
                already_banned_users += 1
                continue

            # Banning
            event.msg.guild.create_ban(
                target,
                reason="Mass banned by IDs."
            )
            banned_users += 1
            sleep(2)


        # Acknowledge
        event.msg.reply(
            Admin.mass_ban.format(
                len(users_to_ban),
                banned_users,
                already_banned_users
            )
        )



    @Plugin.command("channel", group="clean")
    def purge_channel_messages(self, event):

        count = 0
        total_deleted = None

        # Check if user supplied an argument
        if len(event.args):
            try:
                total_deleted = int(event.args[0])
            except ValueError:
                return event.msg.reply(Admin.invalid_arg.format(event.args[0]))


        # Cycle through all messages in channel
        for message in event.channel.messages_iter(
            direction="DOWN",
            bulk=False,
            before=event.msg.id,
            after=None,
            chunk_size=100
        ):

            # Ensure the bot is the author.
            if not message.pinned:

                message.delete()
                count += 1

                # If we have a limit compare it to current
                if total_deleted:

                    # Check limit and if hit, break
                    if count == total_deleted:
                        break

                sleep(5)
        
        return event.msg.reply(Admin.self_cleaned.format(count))
    


    @Plugin.command("user", group="clean")
    def clean_user_messages(self, event):

        count = 0
        total_deleted = None

        # Get arguments for only supplying user
        if len(event.args) >= 1:

            # Get target user ID
            try:
                if len(event.msg.mentions):
                    target_user = event.msg.mentions[0].id
                else:
                    target_user = int(event.args[0])
            except ValueError:
                return event.msg.reply(Admin.invalid_arg.format(event.args[0]))


        # Get arguments for both user and count
        elif len(event.args) == 2:

            # Get user ID
            try:
                if len(event.msg.mentions):
                    target_user = event.msg.mentions[0].id
                else:
                    target_user = int(event.args[0])
            except ValueError:
                return event.msg.reply(Admin.invalid_arg.format(event.args[0]))

            # Get count of messages to delete
            try:
                total_deleted = int(event.args[1])
            except ValueError:
                return event.msg.reply(Admin.invalid_arg.format(event.args[1]))

        # Not enough arguments given to clean channel
        else:
            return event.msg.reply(Admin.nea)


        # Cycle through all messages in channel
        for message in event.channel.messages_iter(
            direction="DOWN",
            bulk=False,
            before=event.msg.id,
            after=None,
            chunk_size=100
        ):

            # Ensure the bot is the author.
            if message.author.id == target_user:

                message.delete()
                count += 1

                # If we have a limit compare it to current
                if total_deleted:

                    # Check limit and if hit, break
                    if count == total_deleted:
                        break

                sleep(1)
        
        return event.msg.reply(Admin.self_cleaned.format(count))



    @Plugin.command("bot", group="clean")
    def clean_bot_messages(self, event):

        count = 0
        total_deleted = None

        # Check if user supplied an argument
        if len(event.args):
            try:
                total_deleted = int(event.args[0])
            except ValueError:
                return event.msg.reply(Admin.invalid_arg.format(event.args[0]))


        # Cycle through all messages in channel
        for message in event.channel.messages_iter(
            direction="DOWN",
            bulk=False,
            before=event.msg.id,
            after=None,
            chunk_size=100
        ):

            # Ensure the bot is the author.
            if message.author.id == self.state.me.id:

                message.delete()
                count += 1

                # If we have a limit compare it to current
                if total_deleted:

                    # Check limit and if hit, break
                    if count == total_deleted:
                        break

                sleep(1)
        
        return event.msg.reply(Admin.self_cleaned.format(count))