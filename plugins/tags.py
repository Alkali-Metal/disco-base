"""
This plugin allows users to be able to create custom commands for within their
guild, in order to modify a tag or remove it, you must have at least the
permission level from the tag itself.
"""

# BOT IMPORTS:
from data.constants import (
    discord_permission_values,
    max_permission_int,
    perm_ints
)
from data.types.bot.plugin_config import PluginConfig
from data.types.bot.guild_config import GuildConfig
from data.constants import bool_true, bool_false
from data.types.discord.embeds import TagEmbed
from data.types.bot.permissions import Perms
from data.types.bot.config import Config
from parser import triggers_commands
from data.response import Tags

# DISCO IMPORTS
from disco.bot import Plugin



default_tags_config ={
    "list": {},
    "options": {
        "log_channel": None,
        "allow_global": True,
        "logging": False
    }
}

tag_fields = [
    "name",
    "response",
    "embed",
    "colour",
    "footer",
    "level",
    "content",
    "url",
    "title",
    "global"
]

mandatory_args = [
    "name",
    "response"
]

arg_defaults = {
    "embed": False,
    "title": None,
    "colour": 0x7289DA,
    "footer": None,
    "level": perm_ints["else"],
    "content": "Tag embed:",
    "url": None,
    "global": False
}

arg_types = {
    "embed": "bool",
    "title": "string",
    "colour": "hex",
    "footer": "string",
    "level": "integer",
    "content": "string",
    "url": "string",
    "global": "bool"
}

illegal_name_characters = [
    "*", "!", "@", "#", "$", "%", "^", "&", "(", ")",
    "[", "]", "{", "}", "?", "\"", "\'", "`", "~", "\\",
    "/", "+", ".", ",", ">", "<", ";", ":", " "
]



def respond_to_tag(event, tag_data):
    msg = event.message
    cmd_args = event.message.content.split()[1:]
    args = [""]

    # Increase each argument's index by one.
    for arg in cmd_args:
        args.append(arg)

    # Check permission level
    if Perms.integer(msg.member) < tag_data["level"]:
        return msg.reply(
            Tags.invalid_perms
        )

    # Set variables
    variables = {
        "name": msg.author.username,
        "count": tag_data["count"],
        "arg": args
    }

    # Check if embedding it
    if tag_data["embed"]:

        

        # Get embed:
        try:
            embed = TagEmbed(
                tag_data,
                variables
            )

            # Try to embed the message
            return msg.reply(
                tag_data["content"],
                embed=embed
            )

        # Error if user didn't supply enough arguments
        except IndexError:
            return msg.reply(Tags.nea)

        # Error if part of the tag embed is missing
        except KeyError:
            msg.reply(Tags.key_missing)
            return msg.reply(tag_data["response"])

        except:
            # Return an embed error
            return msg.reply(
                Tags.embed_error
            )
    else:
        try:
            return msg.reply(
                tag_data["response"].format(
                    **variables
                )
            )

        # Error if user didn't supply enough variables.
        except IndexError:
            msg.reply(Tags.nea)



def argument_convert(key, value):
    # bool type
    if arg_types[key] == "bool":

        # True state
        if value.lower() in bool_true:
            return True

        # False state
        elif value.lower() in bool_false:
            return False

    # string type
    elif arg_types[key] == "string":
        if len(value) != 0:
            return value
        else:
            return None

    # int type
    elif arg_types[key] == "integer":
        try:
            # try int-ing it's face off
            return int(value)
        except:
            if value in perm_ints:
                return perm_ints[value]
            else:
                return

    # hex colour
    elif arg_types[key] == "hex":
        try:
            # try int-ing it's face off
            return int(value, 16)
        except:
            return 



def tag_data_parser(message_content,
                    require_mandatory=True,
                    defaults=True):
    command_args = message_content.split("--")

    tag_data = {}

    # filter through list for proper arguments
    for argument in command_args:
        if "=" in argument:
            key, *value = argument.split("=")
            key = key.lower().strip()
            value = "=".join(value)

            # Ensure argument is a valid argument
            if key in tag_fields:
                tag_data[key] = value.strip()
            else:
                return "InvalidArg-{}-{}".format(
                    key,
                    value
                )


    # Ensure we are erroring if the mandatory args are not given
    if require_mandatory:

        # Filter through mandatory arguments
        for argument in mandatory_args:

            # Ensure mandatory arguments are given
            if argument not in tag_data.keys():
                return "MandatoryMissing-{}".format(
                    argument
                )


    # filter through arguments which have a default value
    for argument in arg_defaults:
        # Ensure we want to assign default values
        if defaults:

            # check if user didn't supply argument then assign default
            if argument not in tag_data.keys():
                tag_data[argument] = arg_defaults[argument]
            
            # user gave the argument, convert to proper datatype
            else:
                tag_data[argument] = argument_convert(
                    argument,
                    tag_data[argument]
                )

        else:
            # ensure the user gave the argument before attempting to convert
            if argument in tag_data.keys():
                tag_data[argument] = argument_convert(
                    argument,
                    tag_data[argument]
                )

    return tag_data


# TODO: Actually use the cleanse text function.
def cleanse_text(text):
    pass



class CustomCommands(Plugin):

    #=======================================#
    # PLUGIN INFORMATION FOR PARSER:
    in_dev = True
    can_reload = True
    restricted = False
    force_default = False
    bypass_enabled = False
    can_be_enabled = True
    plugin_version = 2.0
    config_settings = {
        "tags-logging_channel": "tags|options|log_channel",
        "tags-logging_enabled": "tags|options|logging",
        "tags-allow_global": "tags|options|allow_global"
    }
    plugin_info = [
        "Allows the creation of commands for specific guilds, allows users to",
        "have embedded responses and customize almost the entirety of the",
        "response."
    ]
    commands_config = {
        "tag": {
            "add": {
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}tag add",
                    "--<Field Name>=<Value>..."
                ],
                "info": [
                    "Allows the user to create a custom command for the",
                    "guild, only mandatory fields are `name` and `response`",
                    "all other fields for this command have defaults. Valid",
                    "fields and types are as follows: `name` (String),",
                    "`response` (String), `embed` (Boolean), `colour` (Hex",
                    "code), `footer` (String), `level` (Integer), `content`",
                    "(String), `url` (String), `title` (String), `global`",
                    "(Boolean). For a description of each of these fields",
                    "you can read the documentation more in-depth [here]&",
                    "&(http://discord-bots.rtfd.io/en/latest/plugins/&",
                    "&Tags/#options-list)"
                ]
            },
            "remove":{
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}tag remove",
                    "<Tag Name>",
                    "[Is Global]"
                ],
                "info": [
                    "Allows the user to remove a custom command for the",
                    "guild. Must have the minimum permission as well as",
                    "the permission level of the command at least (Guild",
                    "owner bypasses the command permission level check).",
                    "If `[Is Global]` is set to `true` then you must be a",
                    "global administrator."
                ]
            },
            "modify": {
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [
                    "{pre}tag modify",
                    "--<Field Name>=<Value>..."
                ],
                "info": [
                    "Allows the user to modify a custom command for the",
                    "guild that already exists, the only mandatory field",
                    "is `name` all other fields for this command are ",
                    "optional. Valid fields and types are as follows:",
                    "`name` (String), `response` (String), `embed` (Boolean),",
                    "`colour` (Hex code), `footer` (String), `level` (Integer",
                    "<= `{max_perm_int}`)",
                    ", `content` (String), `url` (String), `title` (String),",
                    "`global` (Boolean). For a description of each of these",
                    "fields you can read the documentation more in-depth",
                    "[here](http://discord-bots.rtfd.io/en/latest/plugins/&",
                    "&Tags/#options-list)"
                ]
            },
            "list": {
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            },
            "setup": {
                "allow_DMs": False,
                "bot_perms": 2048,
                "user_perms": 0,
                "default_level": perm_ints["server_mod"],
                "bypass_user_perms": False,
                "syntax": [],
                "info": []
            }
        }
    }
    #=======================================#


    @Plugin.listen("MessageCreate")
    def tags_parser(self, event):


        # Ensure no commands triggered
        if triggers_commands(self, event):
            return


        guild_tags = GuildConfig.load(event.message.guild.id)
        global_tags = GuildConfig.load("default")
        guild_list = PluginConfig.load("guild_list")

        prefix = Config.load()["bot"]["commands_prefix"]
        both_have = False


        # Ensure message starts with prefix
        if not event.message.content.startswith(prefix):
            return


        command, *args = event.message.content.split()
        command = command[len(prefix):]


        # Check if both the guild and global have a tag of that name
        if command in global_tags["tags"]["list"].keys():
            if command in guild_tags["tags"]["list"].keys():
                both_have = True


        # Ensure guild has global commands allowed
        if guild_tags["tags"]["options"]["allow_global"]:

            # Retrieve tag data
            if command in global_tags["tags"]["list"].keys():
                tag_data = global_tags["tags"]["list"][command]

                # Check if we are embedding the response
                if tag_data["embed"]:

                    # Ensure we have the proper permissions:
                    if not event.message.channel.get_permissions(
                        self.state.me
                    ).can(
                        discord_permission_values["embed_links"]
                    ):
                        return event.message.reply(Tags.embed_error)


                # Respond to command
                response = respond_to_tag(
                    event,
                    tag_data
                )

                # Ensure command doesn't error
                if response.content != Tags.invalid_perms:

                    # Increment counter
                    global_tags["tags"]["list"][command]["count"] += 1

                    GuildConfig.write(
                        "default",
                        global_tags
                    )



        # Ensure guild has tags enabled
        if "CustomCommands" in guild_list[str(event.message.guild.id)]:

            # Ensure the tag isn't in both guild/global
            if both_have:
                return

            # Retrieve tag data
            if command in guild_tags["tags"]["list"].keys():
                tag_data = guild_tags["tags"]["list"][command]
                print(event.channel.get_permissions(self.state.me).to_dict())
                # Check if we are embedding the response
                if tag_data["embed"]:

                    # Ensure we have the proper permissions:
                    if not event.message.channel.get_permissions(
                        self.state.me
                    ).can(
                        discord_permission_values["embed_links"]
                    ):
                        return event.message.reply(Tags.embed_error)


                # Respond to command
                response = respond_to_tag(
                    event,
                    tag_data
                )

                # Ensure command doesn't error
                if response.content != Tags.invalid_perms:

                    # Increment counter
                    guild_tags["tags"]["list"][command]["count"] += 1

                    GuildConfig.write(
                        event.message.guild.id,
                        guild_tags
                    )

        else:
            return event.message.reply(
                Tags.tags_not_enabled
            )



    @Plugin.command("add", group="tag", aliases=["create"])
    def tag_add(self, event):

        tag_data = tag_data_parser(event.msg.content)

        if type(tag_data) == type(""):
            tag_data = tag_data.split("--")

            # Return a value error to the user's face
            if tag_data[0] == "ValueError":
                return event.msg.reply(
                    Tags.invalid_arg.format(
                        tag_data[2]
                    )
                )

            # Mandatory argument missing
            elif tag_data[0] == "MandatoryMissing":
                return event.msg.reply(
                    Tags.arg_needed.format(
                        tag_data[1]
                    )
                )

            # Invalid argument
            elif tag_data[0] == "InvalidArg":
                return event.msg.reply(
                    Tags.invalid_arg.format(
                        tag_data[1]
                    )
                )
            else:
                return event.msg.reply(
                    Tags.error
                )


        # Ensure name doesn't contain any illegal characters
        for char in illegal_name_characters:
            if char in tag_data["name"]:
                return event.msg.reply(
                    Tags.illegal_char.format(
                        "name",
                        char
                    )
                )


        # Ensure level not greater than highest allowed
        if tag_data["level"] > max_permission_int:
            return event.msg.reply(
                Tags.invalid_perm_int.format(
                    max_perm_int
                )
            )

        tag_data["name"] = tag_data["name"].replace(" ", "-")
        # Ensure tag not global
        if not tag_data["global"]:
            data = GuildConfig.load(event.guild.id, True)

            # Ensure guild has been setup for tags
            if "tags" not in data.keys():
                return event.msg.reply(
                    Tags.guild_not_setup
                )

            # Ensure tag doesn't already exist
            if tag_data["name"] in data["tags"]["list"].keys():
                return event.msg.reply(
                    Tags.already_exists.format(
                        tag_data["name"]
                    )
                )

            # Create tag structure
            data["tags"]["list"][tag_data["name"]] = {
                "response": tag_data["response"],
                "embed": tag_data["embed"],
                "colour": tag_data["colour"],
                "content": tag_data["content"],
                "footer": tag_data["footer"],
                "url": tag_data["url"],
                "level": tag_data["level"],
                "title": tag_data["title"],
                "count": 0
            }

            # update guild config
            GuildConfig.write(event.guild.id, data)

        else:
            if Perms.integer(event.msg.member) >= perm_ints["global_admin"]:
                data = GuildConfig.load("default")

                # Ensure tag doesn't already exist
                if tag_data["name"] in data["tags"]["list"].keys():
                    return event.msg.reply(
                        Tags.already_exists.format(
                            tag_data["name"]
                        )
                    )

                # Create tag structure
                data["tags"]["list"][tag_data["name"]] = {
                    "response": tag_data["response"],
                    "embed": tag_data["embed"],
                    "colour": tag_data["colour"],
                    "content": tag_data["content"],
                    "footer": tag_data["footer"],
                    "url": tag_data["url"],
                    "level": tag_data["level"],
                    "count": 0
                }

                # update guild config
                GuildConfig.write("default", data)

            # invalid permission
            else:
                return event.msg.reply(Tags.invalid_perms)

        event.msg.reply(
            Tags.tag_created.format(
                tag_data["name"]
            )
        )



    @Plugin.command("remove", group="tag", aliases=["delete"])
    def tag_delete(self, event):

        # argument checking
        if len(event.args) >= 2:
            tag = event.args[0]

            # global == true
            if event.args[1].lower() in bool_true:
                is_global = True

            # global == False
            elif event.args[1].lower() in bool_false:
                is_global = False

            # invalid argument
            else:
                return event.msg.reply(
                    Tags.invalid_arg.format(
                        event.args[1]
                    )
                )

        # Only tag name given
        elif len(event.args) == 1:
            tag = event.args[0]
            is_global = False
        else:
            return event.msg.reply(Tags.nea)

        # Check if global
        if is_global:
            tags = GuildConfig.load("default")

            # Ensure tag exists as global
            if tag not in tags["tags"]["list"].keys():
                return event.msg.reply(
                    Tags.not_exist.format(
                        tag
                    )
                )
            else:

                # Ensure user has global permissions
                if Perms.integer(event.msg.member) < tag_data["global_admin"]:
                    return event.msg.reply(
                        Tags.invalid_perms
                    )

                # Remove tag and acknowledge
                tag_data = tags["tags"]["list"].pop(tag)
                GuildConfig.write("default", tags)
                return event.msg.reply(
                    Tags.tag_removed.format(
                        tag,
                        tag_data
                    )
                )

        else:
            tags = GuildConfig.load(event.msg.guild.id)
            tag_list = tags["tags"]["list"]

            if "tags" not in tags.keys():
                return event.msg.reply(
                    Tags.guild_not_setup
                )

            # Ensure tag exists as global
            if tag not in tags["tags"]["list"].keys():
                return event.msg.reply(
                    Tags.not_exist.format(
                        tag
                    )
                )

            # Ensure tag is not at global admin+ level
            if tag_list[tag]["level"] < perm_ints["global_admin"]:

                # Ensure the user has >= the tag permission level
                if Perms.integer(event.msg.member) < tag_list[tag]["level"]:
                    return event.msg.reply(
                        Tags.invalid_perms + " You can't remove a tag you can't run."
                    )
                
            # Remove tag and acknowledge
                tag_data = tags["tags"]["list"].pop(tag)
                GuildConfig.write(event.msg.guild.id, tags)
                return event.msg.reply(
                    Tags.tag_removed.format(
                        tag,
                        tag_data
                    )
                )



    @Plugin.command("modify", group="tag", aliases=["edit"])
    def tag_edit(self, event):
        
        # argument checking
        if not len(event.args):
            return event.msg.reply(Tags.nea)
        
        tag_data = tag_data_parser(
            event.msg.content,
            require_mandatory=False,
            defaults=False
        )

        # Ensure name is given so we know what tag to modify
        if "name" not in tag_data.keys():
            return event.msg.reply(
                Tags.arg_needed.format(
                    "name"
                )
            )
        
        # Assign name argument to command
        else:
            command = tag_data.pop("name")


        # Check if we are modifying a global tag or not
        if "global" not in tag_data.keys():
            global_cmd = False
        else:
            global_cmd = tag_data["global"]
        

        # Guild tag
        if not global_cmd:
            tags = GuildConfig.load(event.msg.guild.id,
                                    force_guild=False,
                                    no_guild_default=False)

        # Global tag
        else:

            # Ensure proper permissions for global tags
            if Perms.integer(event.msg.member) < tag_data["global_admin"]:
                return event.msg.reply(
                    Tags.invalid_perms
                )
            
            tags = GuildConfig.load("default")

        # Ensure tag already exists
        if command not in tags["tags"]["list"]:
            return event.msg.reply(
                Tags.not_exist.format(
                    command
                )
            )

        # Cycle through arguments given in command
        for argument in tag_data.keys():
            # Overwrite previous data
            tags["tags"]["list"][command][argument] = tag_data[argument]


        # ensure global
        if global_cmd:
            GuildConfig.write("default", tags)
        else:
            GuildConfig.write(event.msg.guild.id, tags)

        event.msg.reply(
            Tags.tag_updated.format(
                command
            )
        )



    @Plugin.command("list", group="tag")
    def tag_list(self, event):

        tags = GuildConfig.load(event.msg.guild.id)["tags"]
        tag_list = []

        # Ensure there are no tags
        if len(tags["list"].keys()) > 0:

            user_perm_level = Perms.integer(event.msg.member)

            # Cycle through the tags
            for tag in tags["list"].keys():
                
                # Ensure user has proper permissions to run command
                if user_perm_level >= tags["list"][tag]["level"]:
                    tag_list.append(tag)
                else:
                    tag_list.append("*" + tag)

        # ensure guild has global enabled
        if tags["options"]["allow_global"]:
            tags = GuildConfig.load("default")["tags"]
            user_perm_level = Perms.integer(event.msg.member)

            # Cycle through the tags
            for tag in tags["list"].keys():
                
                # Ensure user has proper permissions to run command
                if user_perm_level >= tags["list"][tag]["level"]:
                    tag_list.append(tag)
                else:
                    tag_list.append("*" + tag)

        response = Tags.tag_list.format(
            ", ".join(
                tag_list
            )
        )

        # Ensure that the response isn't too long
        if len(response) <= 2000:
            return event.msg.reply(
                response
            )
        else:
            return event.msg.reply(
                Tags.too_long
            )



    @Plugin.command("setup", group="tag")
    def setup_tags(self, event):

        config = GuildConfig.load(force_guild=True)

        # Ensure guild doesn't have tags setup
        if "tags" not in config.keys():
            config["tags"] = default_tags_config
            return event.msg.reply(
                Tags.guild_setup
            )

        else:
            return event.msg.reply(
                Tags.already_setup
            )