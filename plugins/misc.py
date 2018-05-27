# BOT IMPORTS
from data.response import MiscResponse

# DISCO IMPORTS:
from disco.bot import Plugin


#=============================================================================#
# PLUGIN INITIALIZATION & CONFIGURATION:


class Misc(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = False
    can_reload = True
    restricted = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    config_settings = {}
    plugin_info = [
        "Random commands that don't belong in any other plugin."
    ]
    commands_config = {
        "None": {
            "test": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}test"
                ],
                "info": [
                    "Tests to ensure the bot is online."
                ]
            }
        }
    }
    #=======================================#



    @Plugin.command("test")
    def test_command(self, event):

        event.msg.reply(MiscResponse.test_confirmed)