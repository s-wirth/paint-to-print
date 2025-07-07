import sys
#######################################################################
# General Helper Functions                                 
#######################################################################

# ---------------------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------------------

def pprint(*args, **kwargs):
    pprint('\n')
    print(*args, file=sys.stderr, **kwargs)
    pprint('\n')


def ending_slash(path):
    """
    Adds a trailing slash to a given path if it does not already exist.

    Parameters
    ----------
    path : str
        The path to add the trailing slash to.

    Returns
    -------
    str
        The path with a trailing slash.
    """
    if path[-1] != '/':
        path += '/'
    return path