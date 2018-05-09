from disco.types.message import MessageEmbed

from time import sleep



class Colour:
    GREEN = 0x00AA00
    YELLOW = 0x7289DA
    RED = 0xAA0000
    BLURPLE = 0x7289DA



def TagEmbed(tag_data, variables):
    embed = MessageEmbed()
    embed.title = tag_data["title"]
    embed.description = tag_data["response"].format(
        **variables
    )
    embed.color = tag_data["colour"]
    embed.set_footer(text=tag_data["footer"])
    embed.url = tag_data["url"]
    return embed





#=============================================================================#
# LOG EMBED CREATIONS


class LogEmbeds:

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# CHANNEL EVENTS

    def CHANNEL_CREATE(event):
        sleep(1)

        # Retrieve the audit log object
        data = event.guild.get_audit_log_entries(
            action_type=10,
            limit=1
        )[0]

        # Create log embed
        embed = MessageEmbed()
        embed.title = "Channel Created"
        embed.add_field(name="Channel:",
                        value=event.channel.name,
                        inline=True)
        embed.add_field(name="Type:",
                        value=event.channel.type,
                        inline=True)
        embed.add_field(name="User:",
                        value="<@{}>".format(data.user_id),
                        inline=False)
        embed.color = Colour.GREEN
        return embed


    def CHANNEL_UPDATE(event):
        sleep(1)

        # Retrieve the audit log object
        # (We just have to hope that it is the right object)
        data = event.guild.get_audit_log_entries(
            limit=1
        )[0]

        field_count = 2
        embed = MessageEmbed()
        embed.title = "Channel Updated"
        embed.color = Colour.YELLOW

        # Create static fields
        embed.add_field(name="Channel:",
                        value=event.channel.name,
                        inline=True)
        embed.add_field(name="User:",
                        value="<@{}>".format(data.user_id),
                        inline=True)


        # Filter through all changes
        for change in data.changes:
            print(change.to_dict())
            # Ensure we don't exceed the field limit
            if field_count < 25:

                # Setting deleted
                if change.old_value and not change.new_value:
                    embed.add_field(
                        name="{}:".format(change.key),
                        value="Unset from: `{c.old_value}`".format(c=change),
                        inline=True
                    )

                #Setting modified
                elif change.new_value and change.old_value:
                    embed.add_field(
                        name="{}:".format(change.key),
                        value="From: `{c.old_value}`\nTo: `{c.new_value}`".format(c=change),
                        inline=True
                    )

                # Setting created
                elif change.new_value and not change.old_value:
                    embed.add_field(
                        name="{}:".format(change.key),
                        value="Set to: `{c.new_value}`".format(c=change),
                        inline=True
                    )
            else:
                break
        return embed


    def CHANNEL_DELETE(event):
        sleep(1)

        # Retrieve the audit log object
        data = event.guild.get_audit_log_entries(
            action_type=12,
            limit=1
        )[0]

        # Create log embed
        embed = MessageEmbed()
        embed.title = "Channel Deleted"
        embed.color = Colour.RED

        # Main body of embed
        embed.add_field(name="Channel:",
                        value=event.name,
                        inline=True)
        embed.add_field(name="Type:",
                        value=event.type,
                        inline=True)
        embed.add_field(name="User:",
                        value="<@{}>".format(data.user_id),
                        inline=False)

        return embed


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# MESSAGE EVENTS


    def MESSAGE_DELETE(event):
        sleep(1)

        # Retrieve the audit log object
        data = event.guild.get_audit_log_entries(
            action_type=72,
            limit=1
        )[0]

        # Create log embed
        embed = MessageEmbed()
        embed.title = "Message Deleted"
        embed.color = Colour.RED

        # Main body of embed
        embed.add_field(name="Channel:",
                        value="<#{}>".format(event.channel.id),
                        inline=True)
        embed.add_field(name="Message Author:",
                        value="<@{}>".format(data.user_id),
                        inline=True)

        return embed


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# ROLE EVENTS


    def ROLE_CREATE(event):
        sleep(1)

        # Retrieve the audit log object
        data = event.guild.get_audit_log_entries(
            action_type=30,
            limit=1
        )[0]

        # Create log embed
        embed = MessageEmbed()
        embed.title = "Role Created"
        embed.color = Colour.GREEN

        # Main body of embed
        embed.add_field(name="User:",
                        value="<@{d.user_id}>".format(d=data),
                        inline=True)

        return embed