class Role:
    
    def multi(member, bot, data):
        bot_highest = 0
        guild_roles = member.guild.roles

        #filter through guild roles
        for role_id in guild_roles:

            #is in bot roles
            if role_id in bot.roles:

                #is higher than the already existing highest
                if guild_roles[role_id].position > bot_highest:
                    bot_highest = guild_roles[role_id].position

        #filter through roles in the list to add/remove
        for role in data:

            #is lower than bot's highest?
            if guild_roles[int(role)].position < bot_highest:

                #add or remove?
                if data[role] == "add":
                    member.add_role(int(role))
                elif data[role] == "remove":
                    member.remove_role(int(role))
    
    

    def add(member, data):
        if type(data) == type([]):
            for role in data:
                member.add_role(int(role))
        else:
            member.add_role(int(data))
    

    
    def remove(member, roles):
        if type(data) == type([]):
            for role in data:
                member.remove_role(int(role))
        else:
            member.remove_role(int(data))
    
    
    def exists(guild, role_id=None, role_name=None):
        for role in guild.roles:
            if role_id != None:
                if role.id == role_id:
                    return True
                return False
            elif role_name != None:
                if role.name == role_name:
                    return True
                return False
    
    
    def get(guild, role_id=None, role_name=None):
        roles = []
        for role in guild.roles:
            if role_id != None:
                if role.id == role_id:
                    roles.append(role)
            elif role_name != None:
                if role.name == role_name:
                    roles.append(role)
        return roles


    def filter_by_index(roles):
        index = 0
        highest = 0
        response = ""
        total_iterations = 0

        # cycle through role objects
        for role in roles:
            total_iterations += 1
            if roles[role].position > highest:
                highest = roles[role].position

        # ensure that we cycle through the roles until the current index matches
        #  the highest index
        while index < highest:

            # add a break condition just in case there is a role index missing
            if total_iterations >= 1000:
                break

            # cycle through role objects
            for role in roles:
                total_iterations += 1
                # Ensure role position is same as index
                if roles[role].position == index:

                    # concatenate role data
                    response = str(roles[role].id) + " - " + roles[role].name + "\n" + response
                    index += 1

        return {
            "response": response,
            "iter_count": total_iterations
        }