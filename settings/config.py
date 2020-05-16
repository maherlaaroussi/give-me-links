import platform

class Common(object):
    # Project
    AUTHOR = 'Maher LAAROUSSI'
    VERSION = "v0.7.1"
    NAME = "GML"
    HEADER = NAME + " " + VERSION + " by " + AUTHOR

    # URLs
    URL = "https://www2.tirexo.org"
    URL_MOVIES_ALL = "/films-gratuit/"
    URL_MOVIES_BLURAY1080 = "/films-gratuit/qualite-Blu-Ray+1080p/"
    URL_MOVIES_UHD = "/films-gratuit/qualite-ULTRA+HD+(x265)/"
    URL_MOVIES_FRENCH = "langue-French/"
    URL_MOVIES_VOSTFR = "langue-VOSTFR/"
    URL_MOVIES_MULTI = "langue-MULTI/"
    URL_MOVIES_LANGUAGES_ALL = ""

    # DOM
    MOVIES_PAGES = "/html/body/div[1]/div/div/div/div[3]/div/div/a[2]"
    MOVIES_PAGES_BIS = "/html/body/div[1]/div/div/div/div[2]/div/div/a[2]"
    MOVIES_INFO = [
        ("Title", '/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/h2/b'),
        ("Quality", '/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[1]/span[1]'),
        ("Language", '/html/body/div[1]/div/div/div/div/div/article/div[2]/div/div/div[1]/span[2]')
    ]
    MOVIES_INFO_HREF = [
        ("Link", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[1]/a[1]'),
        ("Date", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[4]'),
        ("Size", '/html/body/div[1]/div/div/div/div[2]/div/article/div[2]/div/div[1]/div[3]/div/table/tbody/tr/td[3]')
    ]
    PROTECTION_CLICK = "/html/body/center/div/div[2]/div/center/form/input"
    PROTECTION_LINK = "/html/body/center/div/div[2]/div/div[1]/a"

    # ComboBox
    QUALITIES = [
                    ('All', URL_MOVIES_ALL),
                    ('Blu-Ray 1080p', URL_MOVIES_BLURAY1080),
                    ('UHD 2160p x265', URL_MOVIES_UHD)
                ]
    LANGUAGES = [
                    ('All', URL_MOVIES_LANGUAGES_ALL),
                    ('Multi', URL_MOVIES_MULTI),
                    ('French', URL_MOVIES_FRENCH),
                    ('VOSTFR', URL_MOVIES_VOSTFR)
                ]
    HOSTS = [
                    ('All'),
                    ('UpToBox'),
                    ('1fichier')
                ]

    # StyleSheet
    font_family = "Carlito"
    COMBOBOX = "background-color: black; border-color: white; color: white; font-size: 18px; font-style: regular; font-family: " + font_family
    BTN_START = "background-color: black; border-width: medium; color: white; font-size: 20px; font-style: bold; font-family: " + font_family
    BTN_QUIT = "background-color: black; border-width: medium; color: white; font-size: 20px; font-style: bold; font-family: " + font_family
    LBL_TITLE = "QLabel {color: white; font-size: 30px; font-family: " + font_family + "}"
    LBL_DESC = "QLabel {color: white; font-size: 14px; font-family: " + font_family + "}"
    LBL_PAGES = "QLabel {color: white; font-size: 16px; font-family: " + font_family + "}"
    LINE = "background-color: black; border-color: white; color: white; font-size: 16px; font-style: regular; font-family: " + font_family

    # OTHERs
    WAITING_TIME = 25
    WAITING = 0.5
    OS_NOW = platform.system()
    JOKES = [
        "go drink a coffee",
        "go watch some movies or tv shows",
        "i like you so fuck off and go eat",
        "shut the fuck off and go drink beers"
    ]

class Local(Common):
    DEBUG = True
    VERBOSE = True
