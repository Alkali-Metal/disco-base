"""
Interacting with bot and user permissions within Discord
"""

# BOT IMPORTS:
from data.constants import discord_permission_values



class Bot:
    def has_perm(api_client, guild, permission):
        bot_user = api_client.users_me_get()

        # single permission
        if type(permission) in (type(""), type(0)):
            return guild.get_member(bot_user).permissions.can(int(permission))


        # needs the entire list of perms
        elif type(permission) == type([]):

            # Get the bot permissions object
            bot_perms = guild.get_member(bot_user).permissions.can

            # Cycle through permissions needed
            for perm in permission:

                # Ensure bot has the permission
                if not bot_perms(int(perm)):
                    return False
            return True



class User:
    def has_perm(member, permission):
        # single user permission
        if type(permission) in (type(""), type(0)):
            return member.permissions.can(int(permission))
        
        # needs entire list of permissions
        elif type(permission) == type([]):

            # Get permission object checking ready
            member_perms = member.permissions.can

            # Cycle through permissions and check
            for perm in permission:

                # Check if user has the permission
                if not member_perms(int(perm)):
                    return False
            return True


class Misc:
    def convert(permission):
        """
        Get's the permission integer value from a string or vice-versa
        """

        # Check if we got a string
        if type(permission) == type(""):

            # Ensure that the permission actually exists.
            if permission in discord_permission_values:
                return discord_permission_values[permission]
            return None


        # Check if we got an integer
        elif type(permission) == type(0):

            # Cycle through all permissions within Discord
            for perm in discord_permission_values:

                # Check if the permission has the correct value then return it
                if discord_permission_values[perm] == permission:
                    return perm
            return None



    def get_list(permission, member, state="all", perm_list=[]):
        """
        Gets a list of permissions the user has or doesn't have
        """

        response = []

        # Get permission object
        perms = member.permissions.to_dict()

        # Get permissions list that the user is allowed
        if state == "has":

            # Cycle through permissions
            for perm in perms:

                # Ensure user has permission
                if not perms[perm]:
                    continue

                # Ensure permission is in list we are comparing to
                if perm in perm_list:
                    response.append(perm)


        # See if we are getting the perms they don't have from the list
        elif state == "needs":

            # Cycle through permissions
            for perm in perms:

                # Ensure user doesn't have permission
                if perms[perm]:
                    continue

                # Ensure permission is in the compare list
                if perm in perm_list:
                    response.append(perm)


        # Returns a list of all permissions the user has
        elif state == "all":
            
            # Cycle through permissions
            for perm in perms:
                
                # Ensure user has permission
                if perms[perm]:
                    response.append(perm)

        return response