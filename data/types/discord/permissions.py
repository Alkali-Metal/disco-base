"""
Interacting with bot and user permissions within Discord
"""


permission_values = {
    "none": 0,
    "administrator": 8,
    "view_audit_log": 128,
    "manage_server": 32,
    "manage_roles": 268435456,
    "manage_channels": 16,
    "kick_members": 2,
    "ban_members": 4,
    "create_instant_invite": 1,
    "change_nickname": 67108864,
    "manage_nicknames": 134217728,
    "manage_emojis": 1073741824,
    "manage_webhooks": 536870912,
    "view_channels": 1024,
    "send_messages": 2048,
    "send_tts_messages": 4096,
    "manage_messages": 8192,
    "embed_links": 16384,
    "attach_files": 32768,
    "read_message_history": 65536,
    "mention_everyone": 131072,
    "use_external_emojis": 262144,
    "add_reactions": 64,
    "connect": 1048576,
    "speak": 2097152,
    "mute_members": 4194304,
    "deafen_members": 8388608,
    "move_members": 16777216,
    "use_voice_activity": 33554432
}



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
            if permission in permission_values:
                return permission_values[permission]
            return None


        # Check if we got an integer
        elif type(permission) == type(0):

            # Cycle through all permissions within Discord
            for perm in permission_values:

                # Check if the permission has the correct value then return it
                if permission_values[perm] == permission:
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