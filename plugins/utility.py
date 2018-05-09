"""
Utility commands that don't really belong in any other plugin that deal with
the backend of the bot. As well as the commands used to edit the guild's
configuration
"""
from data.types.bot.permissions import Perms
from data.types.discord.role import Role
from data.response import Util, Invalid

from disco.types.guild import GuildMember
from disco.types.user import User
from disco.bot import Plugin



valid_settings = {
    "mod_role_ids": "permissions|mod|IDs",
    "mod_role_names": "permissions|mod|names",
    "admin_role_ids": "permissions|admin|IDs",
    "admin_role_names": "permissions|admin|names",
    "cmd_perms": "cmd lvls"
}

no_config_plugins = [
    "MessageParser",
    "ReloadCommand",
    "ConfigEditor",
    "AdminLogging",
    "GlobalAdministration"
]




class UtilCommands(Plugin):

    config_settings = {}


    # Command to get the user's level in the backend of the bot
    @Plugin.command(
        "level",
        aliases=[
            "perms",
            "permissions"
        ],
        group="util"
    )
    def perm_bar_command(self, event):

        # Check if they supplied an argument for the perm level
        if len(event.msg.mentions):
            for k, v in event.msg.mentions.items():
                user = v
                break
        elif len(event.args):
            if event.guild:
                user = event.guild.get_member(event.args[0])
            else:
                return event.msg.reply(Invalid.argument.format(event.args[0]))
        else:
            if event.msg.guild:
                user = event.msg.member
            else:
                user = event.msg.author
        


        # Acknowledge
        if isinstance(user, GuildMember):
            event.msg.reply(
                Util.level.format(
                    user.name,
                    Perms.permission_bar(
                        user
                    )
                )
            )
        elif isinstance(user, User):
            event.msg.reply(
                Util.level.format(
                    user.username,
                    Perms.permission_bar(
                        user
                    )
                )
            )
        else:
            event.msg.reply(
                Util.error
            )


    #@Plugin.command("cmdlevel", group="util")
    def cmd_lvl_getter(self, event):

        # Check arguments
        pass



    @Plugin.command("roles", group="util")
    def role_list_getter(self, event):
        filtered = Role.filter_by_index(event.msg.guild.roles)

        event.msg.reply(
            "```\n" + filtered["response"] +
            "```\n\nTotal iterations: " + str(filtered["iter_count"])
        )



class ConfigEditor(Plugin):

    # Instatiation function
    def init(self):

        # Cycle through loaded plugins retrieving their settings
        for plugin in self.bot.plugins:

            # Ensure plugin actually has config options for 
            if plugin not in no_config_plugins:
                plugin = self.bot.plugins[plugin]
                settings = plugin.config_settings

                # Cycle through settings adding them to the dict
                for setting in settings:
                    valid_settings[setting] = settings[setting]



    @Plugin.command("edit", group="config")
    def edit_config(self, event):
        self.init()
        event.msg.reply("```json\n{}```".format(json.dumps(valid_settings, indent=2)))