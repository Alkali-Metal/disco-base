from disco.bot import Plugin

class BlacklistPlugin(Plugin):
    @Plugin.command("spam")
    def testing_loading(self, event):
        event.msg.reply("eggs")