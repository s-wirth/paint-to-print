import sys

def pprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)