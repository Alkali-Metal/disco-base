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