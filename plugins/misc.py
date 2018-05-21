from data.response import Misc

from disco.bot import Plugin



class Misc(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    config_settings = {}
    commands_config = {
        "None": {
            "test": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False
            }
        }
    }
    #=======================================#



    @Plugin.command("test")
    def test_command(self, event):

        event.msg.reply(Misc.test_confirmed)
        print(self.bot.plugins)