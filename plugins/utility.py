"""
Utility commands that don't really belong in any other plugin that deal with
the backend of the bot. As well as the commands used to edit the guild's
configuration
"""
# BOT IMPORTS:
from data.types.bot.plugin_config import PluginConfig
from data.constants import discord_permission_values
from data.types.bot.guild_config import GuildConfig
from data.types.bot.permissions import Perms
from data.types.bot.config import Config
from data.types.discord.role import Role
from data.response import Util, Invalid

# DISCO IMPORTS:
from disco.types.permissions import PermissionValue
from disco.types.message import MessageEmbed
from disco.types.guild import GuildMember
from disco.types.user import User
from disco.bot import Plugin



# Pre-define config options that are always going to exist.
valid_settings = {
    "mod_role_ids": "permissions|mod|IDs",
    "mod_role_names": "permissions|mod|names",
    "admin_role_ids": "permissions|admin|IDs",
    "admin_role_names": "permissions|admin|names",
    "cmd_perms": "cmd lvls"
}

cmd_list = {}



def filter_perms(member_value, target_value):

    perm_dict = PermissionValue(target_value).to_dict()
    member_perms = PermissionValue(member_value)
    response = ""


    # Ensure we aren't checking against no permissions so that
    #  the response isn't absolutely disgusting
    if target_value != 0:


        # Cycling through permissions dict
        for perm, can in perm_dict.items():

            # Check if permissions is valid
            if can:

                # Ensure user uses permissions
                if member_perms.can(discord_permission_values[perm.lower()]):
                    response = response + "\n+ " + perm.upper()

                else:
                    response = response + "\n- " + perm.upper()

        return response



class Utility(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 0.2
    config_settings = {}
    plugin_info = [
        "This plugin has a variety of useful commands that can provide useful",
        "information, like what a command can do and whether or not the user",
        "is able to execute the command in the guild, and whether or not the",
        "bot has all the required permissions for the command to work properly"
    ]
    commands_config = {
        "util": {
            "level": {
                "allow_DMs": True,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}util level",
                    "[User: user mention | ID]"
                ],
                "info": [
                    "Displays the user's permission level within the bot.",
                    "If no argument supplied uses member who ran the command."
                ]
            },
            "roles": {
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 268435456,
                "default_level": 1,
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}util roles"
                ],
                "info": [
                    "Returns a list of roles and their IDs within the server,",
                    "sorted by their position in the role heirarchy."
                ]
            }
        },
        "info": {
            "cmd": {
                "allow_DMs": True,
                "bot_perms": 18432,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}info cmd",
                    "[Command: Command]"
                ],
                "info": [
                    "Returns help text and syntax for specified command. If",
                    "no command specified it will return this help text."
                ]
            },
            "plugin": {
                "allow_DMs": True,
                "bot_perms": 18432,
                "user_perms": 0,
                "default_level": 0,
                "bypass_user_perms": True,
                "syntax": [
                    "{pre}info cmd",
                    "[Command: Command]"
                ],
                "info": [
                    "Returns the description of the specified plugin. The",
                    "plugin does not need to be enabled in the server for",
                    "this command to work."
                ]
            }
        }
    }
    #=======================================#


    # Instatiation function
    def load(self, ctx):
        
        # Cycle through all commands bot has loaded
        for cmd in self.bot.commands:

            # Check if the command has a group
            if cmd.group:
                cmd_list["{} {}".format(cmd.group, cmd.name)] = cmd
            else:
                cmd_list[cmd.name] = cmd



#=============================================================================#
# COMMANDS:


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



    @Plugin.command("roles", group="util")
    def role_list_getter(self, event):
        filtered = Role.filter_by_index(event.msg.guild.roles)

        event.msg.reply(
            "```\n" + filtered["response"] +
            "```\n\nTotal iterations: " + str(filtered["iter_count"])
        )


#=============================================================================#


    @Plugin.command(
        "cmd",
        group="info",
        aliases=[
            "help"
            "command"
        ]
    )
    def command_info(self, event):

        if Perms.integer(event.msg.member) <= 4:
            return event.msg.reply("This command has been temporarily" + 
            " disabled due to a bug within Disco. Please refrain from " +
            "attempting to use this command while the bug is being fixed.")

        # Check if we received multiple arguments
        if len(event.args) == 1:
            cmd = event.args[0]

        elif len(event.args) >= 2:
            cmd = event.args[0] + " " + event.args[1]

        else:
            cmd = "info cmd"



        # Ensure that supplied command is valid
        if cmd not in cmd_list.keys():
            return event.msg.reply(Util.invalid_arg.format(cmd))


        cmd = cmd_list[cmd]


        me = self.state.me
        me_member = event.guild.get_member(me)


        # Ensure the plugin is enabled in the guild
        if event.guild:
            guilds = PluginConfig.load("guild_list")
            g_id = str(event.guild.id)

            # Ensure guild has been enabled
            if g_id in guilds:

                # Check if the plugin is not enabled
                if cmd.plugin.name not in guilds[g_id]:
                    return event.msg.reply(
                        Util.plugin_not_enabled.format(
                            cmd.plugin.name
                        )
                    )


        # Get command data
        plugin = cmd.plugin


        cmd_config = plugin.commands_config[str(cmd.group)][cmd.name]


        config = GuildConfig.load(event.guild.id)


        try:
            cmd_level = config["cmd_lvls"][plugin.name][str(cmd.group)][cmd.name]
        except KeyError:
            cmd_level = cmd_config["default_level"]


        try:
            bypass_user_perms = config["permissions"]["bypass_user_perms"]
        except KeyError:
            bypass_user_perms = cmd_config["bypass_user_perms"]


        user_level = Perms.integer(event.msg.member)



        user_perms = filter_perms(
            event.channel.get_permissions(event.msg.member),
            cmd_config["user_perms"]
        )

        bot_perms = filter_perms(
            event.channel.get_permissions(me_member),
            cmd_config["bot_perms"]
        )


        cmd_aliases = []
        for name in cmd.triggers:
            cmd_aliases.append(name)


        variables = {
            "pre": Config.load()["bot"]["commands_prefix"],
            "user_username": event.msg.author.username,
            "user_nickname": event.msg.member.name,
            "user_discrim": event.msg.author.discriminator,
            "user_id": event.msg.author.id,
            "bot_username": me.username,
            "bot_nickname": me_member.name,
            "bot_id": me.id,
            "plg_name": plugin.name
        }


        # Format data nicely in an embed
        embed = MessageEmbed()

        embed.title = "{bot_nickname} Help:".format(**variables)
        embed.color = 0x00aa00
        embed.set_footer(
            text="Requested by: {user_username}#{user_discrim} ({user_id})".format(
                **variables
            )
        )

        # Command description
        embed.add_field(
            name="Command Description:",
            value=" ".join(
                cmd_config["info"]
            ).format(
                **variables
            ).replace(
                "& &",
                ""
            ),
            inline=False
        )

        # Command syntax
        embed.add_field(
            name="Command Syntax:",
            value="```" + " ".join(
                cmd_config["syntax"]
            ).format(
                **variables
            ).replace(
                "& &",
                ""
            ) + "```",
            inline=False
        )

        # Check if user permissions are bypassed
        if not bypass_user_perms:

            # Ensure that the permissions didn't return `None`
            if user_perms:

                # Permissions that the user needs to have
                embed.add_field(
                    name="Required User Permissions:",
                    value="Green indicates that the permission requirement is met, red indicates it is not met.\n```diff\n{}\n```".format(user_perms),
                    inline=False
                )

        # Check if we are adding bot permissions
        if user_level >= 1:

            # Ensure that the permissions didn't return `None`
            if bot_perms:
                embed.add_field(
                    name="Required Bot Permissions:",
                    value="Green indicates that the permission requirement is met, red indicates it is not met.\n```diff\n{}\n```".format(bot_perms),
                    inline=False
                )

        # Can the command be ran in Direct Messages
        embed.add_field(
            name="Allowed in DMs:",
            value=cmd_config["allow_DMs"],
            inline=True
        )

        # Whether or not the requestee can run the command
        embed.add_field(
            name="Can Requestee Run It:",
            value=(user_level >= cmd_level),
            inline=True
        )

        # Whether or not this command is bypassing user permissions
        embed.add_field(
            name="Bypasses User Permissions:",
            value=bypass_user_perms,
            inline=True
        )

        # The internal permission level that the bot requires for the user
        embed.add_field(
            name="Permission Level:",
            value=cmd_level,
            inline=True
        )

        # Check if there are actully any aliases before adding it
        if len(cmd_aliases):

            # A list of aliases that the command has
            embed.add_field(
                name="Aliases:",
                value=", ".join(cmd_aliases),
                inline=True
            )

        # Alert user what plugin the command comes from
        embed.add_field(
            name="Plugin Name:",
            value=plugin.name,
            inline=True
        )


        # Respond with the embed
        return event.msg.reply(embed=embed)



class ConfigEditor(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    can_reload = True
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 2.0
    config_settings = None

    commands_config = {
        "<GroupName | None>": {
            "<CommandName>": {
                "allow_DMs": True,
                "bot_perms": 0,
                "user_perms": 0,
                "default_level": 0
            }
        }
    }
    #=======================================#

    # Instatiation function
    def init(self):

        # Cycle through loaded plugins retrieving their settings
        for plugin in self.bot.plugins:

            # Ensure plugin actually has config options for 
            if plugin.config_settings != None:
                plugin = self.bot.plugins[plugin]
                settings = plugin.config_settings

                # Cycle through settings adding them to the dict
                for setting in settings:
                    valid_settings[setting] = settings[setting]



    @Plugin.command("edit", group="config")
    def edit_config(self, event):
        self.init()
        event.msg.reply("```json\n{}```".format(json.dumps(valid_settings, indent=2)))