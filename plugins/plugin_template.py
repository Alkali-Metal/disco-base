# BOT IMPORTS:


# DISCO IMPORTS:
from disco.bot import Plugin

# MISC MODULE IMPORTS:




class PluginName(Plugin):


    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 0.1
    config_settings = None
    plugin_info = []
    commands_config = {
        "<GroupName | None>": {
            "<CommandName>": {
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            }
        }
    }
    #=======================================#


#=============================================================================#
# COMMANDS:


#=============================================================================#
# LISTENERS: