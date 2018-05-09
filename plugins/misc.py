from data.response import Misc

from disco.bot import Plugin

from data.types.bot.permissions import Perms

class MiscCommands(Plugin):

    config_settings = {}


    @Plugin.command("test")
    def test_command(self, event):
        event.msg.reply(Misc.test_confirmed)