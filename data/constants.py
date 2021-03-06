# A mapping of all custom emojis that the bot will use on a regular basis for
#  built-in  command responses. (Tags are excluded here)
custom_emojis = {

    # Red "X" and Green Check mark
    "red_tick": "<:redtick:359072372789215232>",
    "green_tick": "<:greentick:359072286466244609>",

    # Red "-1" and Green "+1"
    "-1": "<:decrease:363848504990367744>",
    "+1": "<:increase:363848505024053248>",

    # Yellow and red Exclamation mark
    "yellow_exclaim": "<:report:383406481162371072>",
    "red_exclaim": "<:reported:383406480939941889>"
}


# Permission ints
perm_ints = {
    "bot_creator":   100,
    "global_admin":    4,
    "server_owner":    3,
    "server_admin":    2,
    "server_mod":      1,
    "else":            0,
    "bots":           -1
}



# The maximum permission integer that users are allowed to use in commands,
#  recommended that it stays one higher than the "global_admin" permission
#  integer.
max_permission_int = 5



# webhook base URLS, used in the logging systems
webhook_base = "https://discordapp.com/api/webhooks/"



# Used in command arguments where we are checking if the user supplied a bool
bool_true = [
    "true",
    "t",
    "1",
    "yes",
    "y",
    ":thumbsup:",
    "👍"
]



# Used in command arguments where we are checking if the user supplied a bool
bool_false = [
    "false",
    "f",
    "0",
    "no",
    "n",
    ":thumbsdown:",
    "👎"
]



# A dictionary which converts strings into Discord permission integers
discord_permission_values = {
    "none": 0,
    "administrator": 8,
    "view_audit_log": 128,
    "manage_server": 32,
    "manage_roles": 268435456,
    "manage_channels": 16,
    "kick_members": 2,
    "ban_members": 4,
    "create_instant_invite": 1,
    "change_nickname": 67108864,
    "manage_nicknames": 134217728,
    "manage_emojis": 1073741824,
    "manage_webhooks": 536870912,
    "view_channels": 1024,
    "send_messages": 2048,
    "send_tts_messages": 4096,
    "manage_messages": 8192,
    "embed_links": 16384,
    "attach_files": 32768,
    "read_message_history": 65536,
    "mention_everyone": 131072,
    "use_external_emojis": 262144,
    "add_reactions": 64,
    "connect": 1048576,
    "speak": 2097152,
    "mute_members": 4194304,
    "deafen_members": 8388608,
    "move_members": 16777216,
    "use_voice_activity": 33554432
}


# Main data path for the JSON handler
base_JSON_path = "data/"


# The number of spaces we should be indenting with in the databases
DB_indent_level = 2


# The valid types of blacklists that are supported
valid_blacklists = [
    "guild",
    "channel",
    "user"
]