"""
This plugin allows git operations from within Discord itself so that the bot
is able to update itself remotely if you do not have SSH access or just don't
want to SSH into the server at the time.
"""
from disco.bot import Plugin

class GitHub(Plugin):

    config_settings = {}


    @Plugin.command("download", group="github", aliases=["dl", "update"])
    def update_bot(self, event):
        pass