import os
from datetime import datetime
import urllib.request

""" Get game directory """
# gameDir = os.getcwd()
gameDir = "G:\\GameData\\RimWorld"
gameId = (
    open(os.path.join(gameDir, "SWconfig.ini"), "r")
    .read()
    .split("Appid = ")[1]
    .split("\n")[0]
)
steamcmd = os.path.join(gameDir, "steamcmd", "steamcmd.exe")
Modfolder = os.path.join(gameDir, "LinkNeverDie.Com-GSE", "mods")
ModRootFolder = os.path.join(
    gameDir, "steamcmd", "steamapps", "workshop", "content", gameId
)


""" unlink mod folder """


def unlink():
    try:
        os.unlink(Modfolder)
    except:
        pass


""" Check date format """


def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


""" Get last update mod from steam workshop web with mod id """


def getLastUpdate(modId):
    fp = urllib.request.urlopen(
        "https://steamcommunity.com/sharedfiles/filedetails/?id=" + modId
    )
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    try:
        mystr = (
            mystr.split('<div class="detailsStatRight">')[3].split("</div>")[0].strip()
        )
        return mystr
    except:
        return "0"


""" get current version mod """


def getCurrentVersion(mod):
    mod_version_file = os.path.join(
        gameDir,
        "steamcmd",
        "steamapps",
        "workshop",
        "content",
        "294100",
        mod,
        "About",
        "timestamp.txt",
    )
    if os.path.exists(mod_version_file) == False:
        mod_version = 0
    else:
        mod_version = open(mod_version_file, encoding="utf8").read()
    return mod_version


""" Check mod version """


def formatDate(current, dateFromWeb):
    if current == 0:
        return True
    if is_valid_date(current, "%d/%m/%Y %H:%M:%S"):
        date1 = datetime.strptime(current, "%d/%m/%Y %H:%M:%S")
    elif is_valid_date(current, "%m/%d/%Y %I:%M:%S %p"):
        date1 = datetime.strptime(current, "%m/%d/%Y %I:%M:%S %p")
    elif is_valid_date(current, "%d %b, %Y @ %I:%M%p"):
        date1 = datetime.strptime(current, "%d %b, %Y @ %I:%M%p")
    elif is_valid_date(current, "%d %b @ %I:%M%p"):
        date1 = datetime.strptime(current, "%d %b @ %I:%M%p")
    elif is_valid_date(current, "%Y-%m-%d %H:%M:%S"):
        date1 = datetime.strptime(current, "%Y-%m-%d %H:%M:%S")
    if is_valid_date(dateFromWeb, "%d %b, %Y @ %I:%M%p"):
        date2 = datetime.strptime(dateFromWeb, "%d %b, %Y @ %I:%M%p")
    if is_valid_date(dateFromWeb, "%d %b @ %I:%M%p"):
        date2 = datetime.strptime(dateFromWeb, "%d %b @ %I:%M%p")
    return date1 < date2
