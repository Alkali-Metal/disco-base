from data.types.bot.guild_config import GuildConfig
from data.types.bot.config import Config
from data.constants import perm_ints



class Perms:


    def integer(member, guild=True):

        # Bot?
        try:
            # member == User
            if member.bot:
                return perm_ints["bots"]
        except:
            # member == GuildMember
            if member.user.bot:
                return perm_ints["bots"]


        # Alkali?
        if member.id == 125793782665969664:
            return perm_ints["bot_creator"]


        # global admin
        elif Perms.is_admin(member, guild=False):
            return perm_ints["global_admin"]


        # check guild-level permissions
        elif guild:

            # server owner
            if member.id == member.guild.owner.id:
                return perm_ints["server_owner"]


            # server admin
            elif Perms.is_admin(member, g_admin=False):
                return perm_ints["server_admin"]


            # server mod
            elif Perms.is_mod(member):
                return perm_ints["server_mod"]

        
        #everyone else
        return perm_ints["else"]


    def permission_bar(member):

        # Get the two values needed for the permission calculations
        perm_level = Perms.integer(member, hasattr(member, "guild")) + 1
        max_perm_level = Config.load()["bot"]["max_permission_int"] + 1

        response = ""

        # Ensure that the bar isn't longer than the max perm level
        if perm_level > max_perm_level:
            perm_level = max_perm_level

        # Indicate the permission level they have
        for i in range(perm_level):
            response = response + "▰"

        # Indicate the permissions that they could get
        for i in range(max_perm_level - perm_level):
            response = response + "▱"

        return response


    def is_admin(member, guild=True, g_admin=True):
        #guild admin
        if guild:
            config = GuildConfig.load(member.guild_id)

            #guild admin via role name
            if Perms.has_role(member,
                              config["permissions"]["admin"]["names"],
                              name=True,
                              id=False):
                return True
            
            #guild admin via role ID
            if Perms.has_role(member, config["permissions"]["admin"]["IDs"]):
                return True

        #global admin
        if g_admin:
            config = Config.load()

            if member.id in config["admin"]["ids"]:
                return True
        
        #alkali?
        if member.id == 125793782665969664:
            return True

        return False



    def is_mod(member):
        config = GuildConfig.load(member.guild_id)

        #role names
        if Perms.has_role(member,
                          config["permissions"]["mod"]["names"],
                          name=True,
                          id=False):
            return True
        #role IDs
        elif Perms.has_role(member, config["permissions"]["mod"]["IDs"]):
            return True

        return False



    def has_role(member, roles, name=False, id=True):
        guild = member.guild
        member_roles = []

        if id:
            member_roles = member.roles
            #filter through roles
            if set(member_roles).intersection(roles):
                return True
        
        if name:
            for role in member.roles:
                if role in guild.roles.keys():
                    member_roles.append(guild.roles[role].name)
            if set(member_roles).intersection(roles):
                return True
        return False