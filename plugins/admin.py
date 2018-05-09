from data.response import Admin

from disco.bot import Plugin



class AdminPlugin(Plugin):

    @Plugin.command("ban")
    @Plugin.command("forceban")
    def ban_user(self, event):

        #argument checking
        if len(event.args) == 1:
            target = event.args[0].strip("<@!>")
            reason = None
        elif len(event.args) >= 2:
            target = event.args[0].strip("<@!>")
            reason = " ".join(event.args[1:])
        else:
            return event.msg.reply(Admin.nea)

        #ensure user isn't trying to ban themselves
        if int(target) == event.msg.author.id:
            return event.msg.reply(Admin.no_ban_self)

        #ensure not already banned
        if int(target) in event.msg.guild.get_bans().keys():
            return event.msg.reply(Admin.already_banned)

        #banning
        event.msg.guild.create_ban(target, reason=reason)
        
        user = event.msg.guild.get_bans()[int(target)].user
        #acknowledge
        event.msg.reply(
            Admin.ban_success.format(
                user.username,
                user.id,
                reason
            )
        )