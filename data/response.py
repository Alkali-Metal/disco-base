redtick = "<:redtick:359072372789215232>"
greentick = "<:greentick:359072286466244609>"



class Parser:
    message_too_long = redtick + ": Response too long. Please try something else."
    guild_not_enabled = redtick + ": This guild is not enabled. Contact a global administrator if you believe this to be an error."
    not_DM_enabled = redtick + ": This command cannot be ran in a direct message."
    not_plugin_enabled = redtick + ": This server does not have the `{}` plugin enabled. Contact a global administrator if you believe this to be an error."
    added_plugin = greentick + ": Added plugin `{}` to guild `{}`."
    bot_perm_missing = redtick + ": Command couldn't be executed due to missing permission(s). Run `{}info {}` to see exactly what permissions the bot and you need to run the command."
    user_perm_missing = redtick + ": Command couldn't be executed due to you missing Discord related permission(s). Run `{}info {}` to see exactly what permissions the bot and you need to run the command."
    unconfigured = "This server has not been configured for this plugin yet."
    generic_error = redtick + ": Something went wrong. Try again later."
    name_error = "There are {} with that name!"
    not_enough_arguments = redtick + ": Not enough arguments."
    docs_url = None



class Invalid:
    int = redtick + ": Invalid integer."
    string = redtick + ": Invalid string."
    plugin = redtick + ": Invalid plugin."
    id = redtick + ": Invalid ID."
    command = redtick + ": Invalid command."
    permissions = redtick + ": Invalid permissions."
    argument = redtick + ": Invalid argument. (`{}`)"




class GlobalAdmin:
    nea = Parser.not_enough_arguments
    message_too_long = Parser.message_too_long
    invalid_int = Invalid.int
    invalid_plugin = Invalid.plugin + " (`{}`)"
    invalid_arg = Invalid.argument
    cannot_be_enabled = redtick + ": Plugin `{}` cannot be enabled."
    added_plugin = greentick + ": Added plugin `{}` to guild `{}`."
    removed_plugin = greentick + ": Removed plugin `{}` from guild `{}`."
    plugin_list = "Enabled plugins for guild `{}`:\n```{}```"
    plugin_already_enabled = redtick + ": `{}`(guild) already has the `{}` plugin enabled."
    plugin_not_enabled = redtick + ": Cannot disable plugin `{}` that is not enabled in guild `{}`."
    error = Parser.generic_error
    no_list_zero = redtick + ": I cannot list 0 {} to you."
    start_too_big = redtick + ": Initial index too high, start lower. (Max: `{}`)"
    guild_already_enabled = redtick + ": Guild `{}` is already enabled."
    guild_not_enabled = redtick + ": Guild `{}` isn't enabled."
    guild_enabled = greentick + ": Guild `{}` has been enabled."
    guild_disabled = greentick + ": Guild `{}` has been disabled."
    guild_list = "Enabled guilds:\n```{}```"
    reloaded_plugins = "The following plugins have been reloaded: ```\n{}\n```"
    invalid_plugins = "The following plugins are invalid: ```\n{}\n```"
    didnt_reload_plugins = "The following plugins cannot be reloaded: ```\n{}\n```"
    reload_too_long = "The response was too long, but the task complete"



class Admin:
    nea = Parser.not_enough_arguments
    invalid_perms = Invalid.permissions
    invalid_arg = Invalid.argument
    cant_messages = "Cannot manage messages. Make sure I have the `Manage Messages` permission."
    channel_purged = "Channel (`{}`) has been purged."
    ban_error = Parser.generic_error
    no_ban_self = redtick + ": You cannot ban yourself"
    already_banned = redtick + ": That user is already banned."
    ban_success = greentick + ": {} (`{}`) has been banned with reason: `{}`"
    mass_ban = greentick + ": From a total of `{}` users given.\n\nBanned: `{}`\nAlready Banned: `{}`"
    ban_success_nameless = greentick + ": User `{}` has been banned with reason: `{}`"
    self_cleaned = greentick + ": Cleaned `{}` messages."



class Blacklist:
    invalid_perms = Invalid.permissions
    nea = Parser.not_enough_arguments
    already_blacklisted = "The entity `{}` is already in the specified blacklist with reason: `{}`"
    not_blacklisted = "The entity `{}` cannot be un-blacklisted as it is not blacklisted."
    blacklisted = "Entity `{}` has been added to the `{}` blacklist with reason: `{}`"
    unblacklisted = "Entity `{}` has been removed from the `{}` blacklist."



class Tags:
    nea = Parser.not_enough_arguments
    invalid_arg = Invalid.argument
    invalid_perms = Invalid.permissions
    error = Parser.generic_error
    illegal_char = redtick + ": Illegal character in `{}`. (`{}`)"
    key_missing = redtick + ": Missing key for embed. Reverting to plaintext response."
    already_setup = redtick + ": This guild has already been setup for tags."
    guild_setup = greentick + ": Guild has been setup."
    invalid_perm_int = redtick + ": Permission integer too high. (Max: `{}`)"
    tags_not_enabled = redtick + ": Tags are not enabled within this guild. Contact a global administrator if you believe this to be an error."
    guild_not_setup = redtick + ": This guild does not have the tag system setup. Please run `{}tag setup` to setup the tags system."
    arg_needed = redtick + ": Missing argument. (`{}`)"
    already_exists = redtick + ": Tag with name `{}` already exists."
    tag_created = greentick + ": Created tag with name `{}`."
    tag_removed = greentick + ": Removed tag with name `{}`. Data: ```json\n{}```"
    tag_updated = greentick + ": Updated tag with name `{}`."
    embed_error = redtick + ": Cannot respond to tag. Missing Permission. (`Embed Links`)"
    tag_list = "List of tags: ```\n{}```\nCommands with an `*` in front of the name cannot be ran by you."
    not_exist = redtick + ": Tag `{}` doesn't exist."
    too_long = Parser.message_too_long



class VoicelessRoles:
    invalid_perms = Invalid.permissions
    invalid_ID = Invalid.id
    error = Parser.generic_error
    nea = Parser.not_enough_arguments
    no_DMs = Parser.not_DM_enabled
    not_enabled = Parser.not_plugin_enabled
    guild_setup = greentick + ": Guild has been set up to use automated voiceless roles!"
    already_setup = redtick + ": This guild is already setup for automated voiceless roles."
    not_setup = redtick + ": This guild hasn't been setup yet!"
    no_remove_default = redtick + ": Cannot remove the default role mapping!"
    channel_name_error = redtick + ": " + Parser.name_error.format("multiple voice channels")
    channel_not_found = redtick + ": No voice channels found."
    role_name_error = redtick + ": " + Parser.name_error.format("multiple roles")
    role_not_found = redtick + ": No roles found."
    removed_default = greentick + ": Default role mapping removed. (Set to `None`)"
    updated_default = greentick + ": Default role mapping changed to: `{}`"
    removed_channel_role = greentick + ": `{}`'s role mapping has been removed. (Set to `None`)"
    updated_channel = greentick + ": `{}`'s role mapping changed to: `{}`"
    create_channel_none = greentick + ": Removed role for users in channel `{}` (Set to `None`)"
    create_channel_role = greentick + ": Created channel mapping for channel `{}` and set to role: `{}`"
    removed_channel_mapping = greentick + ": Deleted channel mapping for `{}`. (Will use default mapping)"
    channel_mapping_not_exist = redtick + ": Cannot remove a mapping for channel that doesn't have one."


class Util:
    error = Parser.generic_error
    invalid_arg = Invalid.argument
    nea = Parser.not_enough_arguments
    level = "{}'s permission level: `{}`"
    plugin_not_enabled = redtick + ": This guild does not have the `{}` plugin enabled and hence, cannot access it's help from within this server."


class MiscResponse:
    test_confirmed = "Test confirmed:tm:"
    ipie_boop = "<@230889918094639107>, well hello there."



class Logging:
    nea = Parser.not_enough_arguments
    guild_not_setup = Parser.unconfigured
    missing_perm = Invalid.permissions + " (`{}`)"
    invalid_webhook = redtick + ": That webhook doesn't appear to exist... try again."
    invalid_log_type = redtick + ": Invalid log type. (`{}`)"
    message_delete_error = "Your command appears to have the token in the URL, so I tried to remove it but I am missing the `Manage Messages` permission, I would recommend deleting your command message as people are able to be malicious with the webhook if they have the token as that is what allows programs to be able to send information to the webhook."
    not_log = redtick + ": The webhook `{}` is not a log, so you can't remove it."
    already_log = redtick + ": The webhook `{}` is already logging to a channel."
    webhook_added = greentick + ": Log webhook `{}` added with log type `{}`."
    webhook_removed = greentick + ": Log webhook `{}` removed."
    event_invalid = "The following events were invalid:```{}```"
    event_added = "The following events were added to the log: `{}`"

    moderate_response_format = "========================\n**[{event}]\n{data}"
    compact_response_format = "**[{event}]** {data}"


    class moderate:
        def CHANNEL_CREATE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=10,
                limit=1
            )[0]
            username = event.guild.get_member(data.user_id).user.username
            return "========================\n**[Channel Created]**\nChannel: {e.name} (`{e.id}`).\nUser: {u} (`{d.user_id}`)".format(u=username, d=data, e=event)


        def CHANNEL_UPDATE(event):
            # Retrieve audit log info
            # (We just have to hope that it is the right object because I'm too lazy to ensure it is right)
            data = event.guild.get_audit_log_entries(
                limit=1
            )[0]
            username = event.guild.get_member(data.user_id).user.username
            response = "========================\n**[Channel Updated]**\nChannel: {e.name} (`{e.id}`)\nUser: {u} (`{d.user_id}`)\n"

            #Filter through all the changes made and get the 
            if data.target_id == event.channel.id:
                response = response + "\n\n__Changes__:"

                # Append a change string for each change made
                for change in data.changes:

                    # Setting deleted
                    if change.old_value and not change.new_value:
                        response = response + "\nUnset `{c.key}`".format(c=change)

                    #Setting modified
                    elif change.new_value and change.old_value:
                        response = response + "\nChanged `{c.key}` to `{c.new_value}` from `{c.old_value}`".format(c=change)

                    # Setting created
                    elif change.new_value and not change.old_value:
                        response = response + "\nSet `{c.key}` to `{c.new_value}`".format(c=change)

            return response.format(u=username, d=data, e=event)


        def CHANNEL_DELETE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=12,
                limit=1
            )[0]
            username = event.guild.get_member(data.user_id).user.username
            return "========================\n**[Channel Deleted]**\nChannel: {e.name} (`{e.id}`).\nUser: {u} (`{d.user_id}`)".format(u=username, d=data, e=event)
        

        def MESSAGE_DELETE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=72,
                limit=1
            )[0]

            username = event.guild.get_member(data.user_id).user.username
            return "========================\n**[Message Deleted]**\nChannel: {e.channel.mention} (`{e.channel.id}`)\nMessage Author: {u} (`{d.user_id}`)".format(u=username, d=data, e=event)


        def ROLE_CREATE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=30,
                limit=1
            )[0]

            username = event.guild.get_member(data.user_id).user.username
            return "========================\n**[Role Created]**\nCreated by: {u} (`{d.user_id}`)".format(e=event, u=username, d=data)


    class compact:
        def CHANNEL_CREATE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=10,
                limit=1
            )[0]

            username = event.guild.get_member(data.user_id).user.username
            return "**[Channel Created]** {e.name} (`{e.id}`). User: ".format(e=event)


        def CHANNEL_UPDATE(event):
            # Retrieve audit log info
            # (We just have to hope that it is the right object)
            data = event.guild.get_audit_log_entries(
                limit=1
            )[0]

            username = event.guild.get_member(data.user_id).user.username
            return "**[Channel Updated]** Channel: {e.name} (`{e.id}`). User: {u} (`{d.user_id}`)".format(e=event, d=data, u=username)


        def CHANNEL_DELETE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=10,
                limit=1
            )[0]

            return "**[Channel Deleted]** Channel: {e.name} (`{e.id}`).  User: {u} (`{d.user_id}`)".format(u=username, d=data, e=event)


        def MESSAGE_DELETE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=72,
                limit=1
            )[0]

            username = event.guild.get_member(data.user_id).user.username
            return "**[Message Deleted]** In channel {e.channel.mention}. (Author: {u} `{d.user_id}`)".format(u=username, d=data, e=event)


        def ROLE_CREATE(event):
            # Retrieve audit log info
            data = event.guild.get_audit_log_entries(
                action_type=30,
                limit=1
            )[0]
            username = event.guild.get_member(data.user_id).user.username
            return "**[Role Created]** Created by: {u} (`{d.user_id}`)".format(u=username, d=data)