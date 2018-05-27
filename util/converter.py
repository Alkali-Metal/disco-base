"""
Functions used to convert data from one type to another.
"""
# BOT IMPORTS:
from data.constants import (
    max_perm_int,
    bool_false,
    perm_ints,
    bool_true
)

# DISCO IMPORTS:


# MISC IMPORTS:


#=============================================================================#
# FUNCTIONS:


# convert 'self' to guild id
def from_self(arg, msg):
    if arg.lower() == "self":
        return msg.guild.id


# Convert to boolean
def to_bool(arg):
    return (arg in bool_true)


# Convert to string
def to_string(arg):
    return str(arg)