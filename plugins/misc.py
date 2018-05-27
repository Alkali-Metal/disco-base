# BOT IMPORTS
from data.response import MiscResponse

# DISCO IMPORTS:
from disco.bot import Plugin

# MISC IMPORTS:
from time import sleep


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
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}test"
                ],
                "info": [
                    "Tests to ensure the bot is online."
                ]
            },
            "count": {
                "allow_DMs": False,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 5,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            },
            "stop_count": {
                "allow_DMs": False,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 4,
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            }
        },
        "emoji": {
            "jumbo": {
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}emoji jumbo",
                    "<Emoji: emoji>"
                ],
                "info": [
                    "Enlarges an emoji."
                ]
            }
        }
    }
    #=======================================#

    counting = True

#=============================================================================#
# COMMANDS:



    @Plugin.command("test")
    def test_command(self, event):
        print(self.bot.plugins)
        return event.msg.reply(MiscResponse.test_confirmed)



    @Plugin.command("jumbo", group="emoji", aliases=["enlarge", "big"])
    def emoji_jumbo(self, event):
        return event.msg.reply("Command has not yet been implemented.")



    @Plugin.command("count")
    def count_up(self, event):
        number = int(event.args[0])
        self.counting = True
        while self.counting:
            number += 1
            event.msg.reply(number)
            sleep(5)



    @Plugin.command("stop_count")
    def stop_counting(self, event):
        self.counting = False