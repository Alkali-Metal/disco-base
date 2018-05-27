# BOT IMPORTS:
from data.constants import (,
    max_perm_int,
    perm_ints
)

# DISCO IMPORTS:
from disco.bot import Plugin

# MISC MODULE IMPORTS:



# Pre-define config options that are always going to exist.
valid_settings = {
    "mod_role_ids": "permissions|mod|IDs",
    "mod_role_names": "permissions|mod|names",
    "admin_role_ids": "permissions|admin|IDs",
    "admin_role_names": "permissions|admin|names",
    "cmd_perms": "cmd lvls"
}


#=============================================================================#


class ConfigEditor(Plugin):


    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = True
    can_reload = True
    restricted = False
    force_default = False
    bypass_enabled = True
    can_be_enabled = False
    plugin_version = 0.1
    config_settings = None
    plugin_info = [
        "The built-in editor for the configuration of the bot on a per-guild",
        "basis."
    ]
    commands_config = {
        "config": {
            "edit": {
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            },
            "show": {
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

    # Instatiation function
    def load(self):

        # Cycle through loaded plugins retrieving their settings
        for plugin in self.bot.plugins:

            # Ensure plugin actually has config options for 
            if (
                (plugin.config_settings != None)
                and
                (plugin.config_settings != {})
            ):
                plugin = self.bot.plugins[plugin]
                settings = plugin.config_settings

                # Cycle through settings adding them to the dict
                for setting in settings:
                    valid_settings[setting] = settings[setting]



    @Plugin.command("edit", group="config")
    def edit_config(self, event):
        self.init()
        event.msg.reply("```json\n{}```".format(json.dumps(valid_settings, indent=2)))