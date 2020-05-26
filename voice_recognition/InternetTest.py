import timeit

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def CheckingConnectionToGoogle():
    starttime = timeit.default_timer()
    try:
        html = urlopen("http://www.google.com/").read()
        ConnectionTime = timeit.default_timer() - starttime
        return True, ConnectionTime
    except:
        return False
