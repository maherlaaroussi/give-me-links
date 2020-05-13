import platform

class Common(object):
    # Project
    AUTHOR = 'Maher LAAROUSSI'
    VERSION = "v0.1"
    NAME = "GML"
    HEADER = NAME + " " + VERSION + " by " + AUTHOR

    # URLs
    URL = "https://www2.tirexo.com"
    URL_MOVIES_ALL = "/films-gratuit/"
    URL_MOVIES_BLURAY1080 = "/films-gratuit/qualite-Blu-Ray+1080p/"
    URL_MOVIES_UHD = "/films-gratuit/qualite-ULTRA+HD+(x265)/"
    URL_MOVIES_FRENCH = "langue-French/"
    URL_MOVIES_VOSTFR = "langue-VOSTFR/"
    URL_MOVIES_MULTI = "langue-MULTI/"

    # OTHERs
    WAITING_TIME = 25
    WAITING = 0.5
    OS_NOW = platform.system()

class Local(Common):
    DEBUG = True
    VERBOSE = True
