from data.constants import custom_emojis as emoji

redtick = emoji["red_tick"]
greentick = emoji["green_tick"]



class Parser:
    # A:
    added_plugin = greentick + ": Added plugin `{}` to guild `{}`."
    # B:
    bot_perm_missing = redtick + ": Command couldn't be executed due to missing permission(s). Run `{}info {}` to see exactly what permissions the bot and you need to run the command."
    # C:
    # D:
    docs_url = None
    # E:
    # F:
    # G:
    generic_error = redtick + ": Something went wrong. Try again later."
    guild_not_enabled = redtick + ": This guild is not enabled. Contact a global administrator if you believe this to be an error."
    # H:
    # I:
    # J:
    # K:
    # L:
    # M:
    message_too_long = redtick + ": Response too long. Please try something else."
    # N:
    name_error = "There are {} with that name!"
    not_enough_arguments = redtick + ": Not enough arguments."
    not_DM_enabled = redtick + ": This command cannot be ran in a direct message."
    not_plugin_enabled = redtick + ": This server does not have the `{}` plugin enabled. Contact a global administrator if you believe this to be an error."
    # O:
    # P:
    plugin_in_dev = redtick + ": Cannot run a plugin that is in development in a production bot unless the guild is development enabled."
    # Q:
    # R:
    restricted = redtick + ": Cannot run that command as it is from a restricted plugin. Talk to the global admins about having your guild un-restricted."
    # S:
    # T:
    # U:
    unconfigured = "This server has not been configured for this plugin yet."
    user_perm_missing = redtick + ": Command couldn't be executed due to you missing Discord related permission(s). Run `{}info {}` to see exactly what permissions the bot and you need to run the command."
    # V:
    # W:
    # X:
    # Y:
    # Z:



class Invalid:
    # A:
    argument = redtick + ": Invalid argument. (`{}`)"
    # B:
    # C:
    command = redtick + ": Invalid command."
    # D:
    # E:
    # F:
    # G:
    # H:
    # I:
    id = redtick + ": Invalid ID."
    int = redtick + ": Invalid integer."
    # J:
    # K:
    # L:
    # M:
    # N:
    # O:
    # P:
    permissions = redtick + ": Invalid permissions."
    plugin = redtick + ": Invalid plugin."
    # Q:
    # R:
    # S:
    string = redtick + ": Invalid string."
    # T:
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:



class GlobalAdmin:
    # A:
    added_plugin = greentick + ": Added plugin `{}` to guild `{}`."
    # B:
    blacklisted = greentick + ": Added `{}` (entity) to the `{}` blacklist with reason `{}`"
    # C:
    cannot_be_enabled = redtick + ": Plugin `{}` cannot be enabled."
    cannot_leave = redtick + ": Cannot leave an admin level guild."
    # D:
    didnt_reload_plugins = "The following plugins cannot be reloaded: ```\n{}\n```"
    # E:
    entity_already_blacklisted = redtick + ": `{}` (entity) already in the `{}` blacklist."
    entity_not_blacklisted = redtick + ": `{}` (entity) not in the `{}` blacklist."
    error = Parser.generic_error
    # F:
    # G:
    guild_already_enabled = redtick + ": Guild `{}` is already enabled."
    guild_disabled = greentick + ": Guild `{}` has been disabled."
    guild_enabled = greentick + ": Guild `{}` has been enabled."
    guild_list = "Guild List: ```diff\n{}\n```"
    guild_not_enabled = redtick + ": Guild `{}` isn't enabled."
    # H:
    # I:
    invalid_arg = Invalid.argument
    invalid_blacklist = redtick + ": Invalid blacklist type. (`{}`)"
    invalid_int = Invalid.int
    invalid_plugin = Invalid.plugin + " (`{}`)"
    invalid_plugins = "The following plugins are invalid: ```\n{}\n```"
    # J:
    # K:
    # L:
    # M:
    message_too_long = Parser.message_too_long
    # N:
    nea = Parser.not_enough_arguments
    no_DMs = redtick + ": Cannot leave a guild from DMs without the ID."
    no_list_zero = redtick + ": I cannot list 0 {} to you."
    # O:
    # P:
    plugin_list = "Enabled plugins for guild `{}`:\n```diff\n{}```"
    plugin_already_enabled = redtick + ": `{}`(guild) already has the `{}` plugin enabled."
    plugin_not_enabled = redtick + ": Cannot disable plugin `{}` that is not enabled in guild `{}`."
    # Q:
    # R:
    removed_plugin = greentick + ": Removed plugin `{}` from guild `{}`."
    reloaded_plugins = "The following plugins have been reloaded: ```\n{}\n```"
    reload_too_long = "The response was too long, but the task complete"
    # S:
    start_too_big = redtick + ": Initial index too high, start lower. (Max: `{}`)"
    # T:
    # U:
    unblacklisted = greentick + ": `{}` (entity) removed from the `{}` blacklist."
    # V:
    # W:
    # X:
    # Y:
    # Z:



class Admin:
    # A:
    already_banned = redtick + ": That user is already banned."
    # B:
    ban_error = Parser.generic_error
    ban_success = greentick + ": {} (`{}`) has been banned with reason: `{}`"
    ban_success_nameless = greentick + ": User `{}` has been banned with reason: `{}`"
    # C:
    cant_messages = "Cannot manage messages. Make sure I have the `Manage Messages` permission."
    channel_purged = "Channel (`{}`) has been purged."
    # D:
    # E:
    # F:
    # G:
    # H:
    # I:
    invalid_arg = Invalid.argument
    invalid_perms = Invalid.permissions
    # J:
    # K:
    # L:
    # M:
    mass_ban = greentick + ": From a total of `{}` users given.\n\nBanned: `{}`\nAlready Banned: `{}`"
    # N:
    nea = Parser.not_enough_arguments
    no_ban_self = redtick + ": You cannot ban yourself"
    # O:
    # P:
    # Q:
    # R:
    # S:
    self_cleaned = greentick + ": Cleaned `{}` messages."
    # T:
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:



class Blacklist:
    # A:
    already_blacklisted = "The entity `{}` is already in the specified blacklist with reason: `{}`"
    # B:
    blacklisted = "Entity `{}` has been added to the `{}` blacklist with reason: `{}`"
    # C:
    # D:
    # E:
    # F:
    # G:
    # H:
    # I:
    invalid_perms = Invalid.permissions
    # J:
    # K:
    # L:
    # M:
    # N:
    nea = Parser.not_enough_arguments
    not_blacklisted = "The entity `{}` cannot be un-blacklisted as it is not blacklisted."
    # O:
    # P:
    # Q:
    # R:
    # S:
    # T:
    # U:
    unblacklisted = "Entity `{}` has been removed from the `{}` blacklist."
    # V:
    # W:
    # X:
    # Y:
    # Z:



class Tags:
    # A:
    already_exists = redtick + ": Tag with name `{}` already exists."    
    already_setup = redtick + ": This guild has already been setup for tags."
    arg_needed = redtick + ": Missing argument. (`{}`)"
    # B:
    # C:
    # D:
    # E:
    embed_error = redtick + ": Cannot respond to tag. Missing Permission. (`Embed Links`)"
    error = Parser.generic_error
    # F:
    # G:
    guild_not_setup = redtick + ": This guild does not have the tag system setup. Please run `{}tag setup` to setup the tags system."
    guild_setup = greentick + ": Guild has been setup."
    # H:
    # I:
    illegal_char = redtick + ": Illegal character in `{}`. (`{}`)"
    invalid_arg = Invalid.argument
    invalid_perms = Invalid.permissions
    invalid_perm_int = redtick + ": Permission integer too high. (Max: `{}`)"
    # J:
    # K:
    key_missing = redtick + ": Missing key for embed. Reverting to plaintext response."
    # L:
    # M:
    # N:
    nea = Parser.not_enough_arguments
    not_exist = redtick + ": Tag `{}` doesn't exist."
    # O:
    # P:
    # Q:
    # R:
    # S:
    # T:
    tag_created = greentick + ": Created tag with name `{}`."
    tag_list = "List of tags: ```\n{}```\nCommands with an `*` in front of the name cannot be ran by you."
    tag_removed = greentick + ": Removed tag with name `{}`. Data: ```json\n{}```"
    tag_updated = greentick + ": Updated tag with name `{}`."
    tags_not_enabled = redtick + ": Tags are not enabled within this guild. Contact a global administrator if you believe this to be an error."
    too_long = Parser.message_too_long
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:



class VoicelessRoles:
    # A:
    # B:
    # C:
    # D:
    # E:
    # F:
    # G:
    # H:
    # I:
    # J:
    # K:
    # L:
    # M:
    # N:
    # O:
    # P:
    # Q:
    # R:
    # S:
    # T:
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:
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
    # A:
    # B:
    # C:
    cmd_list = "A list of all commands enabled within the guild: ```{list}``` For more information on a command, run `{pre}cmd info [Command]`"
    # D:
    # E:
    error = Parser.generic_error
    # F:
    # G:
    # H:
    # I:
    invalid_arg = Invalid.argument
    # J:
    # K:
    # L:
    level = "{}'s permission level: `{}`"
    # M:
    # N:
    nea = Parser.not_enough_arguments
    # O:
    # P:
    plugin_not_enabled = redtick + ": This guild does not have the `{}` plugin enabled and hence, cannot access it's help from within this server."
    # Q:
    # R:
    # S:
    # T:
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:



class MiscResponse:
    # A:
    # B:
    # C:
    # D:
    # E:
    # F:
    # G:
    # H:
    # I:
    # J:
    # K:
    # L:
    # M:
    # N:
    # O:
    # P:
    # Q:
    # R:
    # S:
    # T:
    test_confirmed = "Test confirmed:tm:"
    # U:
    # V:
    # W:
    # X:
    # Y:
    # Z:



###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
################################### WARNING ###################################
################### BEYOND THIS POINT IS DEATH AND SADNESS ####################
################### IT CONTAINS A LOT OF UN-COMMENTED CODE ####################
################# YOU HAVE BEEN WARNED: PROCEED AT OWN RISK! ##################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################




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