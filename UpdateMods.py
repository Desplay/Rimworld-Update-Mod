import os
import subprocess
from datetime import datetime
import urllib.request

""" Get game directory """
gameDir = os.getcwd()
gameId = open(os.path.join(gameDir, "SWconfig.ini"), "r").read().split("Appid = ")[1].split("\n")[0]
steamcmd = os.path.join(gameDir, "steamcmd", "steamcmd.exe")
Modfolder = os.path.join(gameDir, "LinkNeverDie.Com-GSE", "mods")
ModRootFolder = os.path.join(gameDir, "steamcmd", "steamapps", "workshop", "content", gameId)

""" Get all mod in folder """
mods = [
    name
    for name in os.listdir(ModRootFolder)
    if os.path.isdir(os.path.join(ModRootFolder, name))
]

""" unlink mod folder """
def unlink():
    try:
        os.unlink(Modfolder)
    except:
        pass
unlink()

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


""" update mod """


def update_mods(modslist):
    modUpdate = ""
    for mod in modslist:
        if formatDate(getCurrentVersion(mod), getLastUpdate(mod)):
            print("update mod: " + mod)
            modUpdate = modUpdate + " +workshop_download_item 294100 " + mod
    print("start update mod, all mod will be updating in one time, please wait...")
    messageInByte = subprocess.run(
        steamcmd + " +login anonymous" + modUpdate + " +quit",
        capture_output=True,
        shell=True,
    ).stdout.splitlines()
    message = []
    for m in messageInByte:
        message.append(m.decode("utf-8"))
    return message


def Handling():
    message = update_mods(mods)
    modError = []
    NOT_ERROR = True
    if os.path.exists(os.path.join("UpdateMod", "logs.txt")):
        os.remove(os.path.join("UpdateMod", "logs.txt"))
    if os.path.exists(os.path.join("UpdateMod", "RawLogs.txt")):
        os.remove(os.path.join("UpdateMod", "lawLogs.txt"))
    if not os.path.exists(os.path.join(os.path.join("UpdateMod"))):
        os.mkdir(os.path.join("UpdateMod"))
    logFile = open(os.path.join("UpdateMod", "logs.txt"), "a")
    rawLogFile = open(os.path.join("UpdateMod", "lawLogs.txt"), "a")
    for m in message:
        if "ERROR" in m:
            NOT_ERROR = False
            logFile.write(m.split(".")[0] + "\n")
            modError.append(m.split("item")[1].split("failed")[0].split(" ")[1])
            print(m.split("item")[1].split("failed")[0].split(" ")[1])
        if "Success" in m:
            modId = m.split("item")[1].split("to")[0].split(" ")[1]
            mod_About = os.path.join(
                gameDir,
                "steamcmd",
                "steamapps",
                "workshop",
                "content",
                "294100",
                modId,
                "About",
                "About.xml",
            )
            openFile = open(mod_About, encoding="utf8").read()
            time_stamp_file = os.path.join(
                gameDir,
                "steamcmd",
                "steamapps",
                "workshop",
                "content",
                "294100",
                modId,
                "About",
                "timestamp.txt",
            )
            if not os.path.exists(time_stamp_file):
                open(time_stamp_file, "a").write(getLastUpdate(modId))
            modname = openFile.split("</name>")[0].split("<name>")[1]
            logFile.write(
                m.split("to")[0] + "( " + modname + " )" + " successfully ! \n"
            )
            print(m.split("to")[0] + "( " + modname + " )" + " successfully ! \n")
    if not NOT_ERROR:
        logFile.write("please update error mod manual" + "\n")
        logFile.write("list mod error: \n")
        for mod in modError:
            logFile.write(mod + "\n")
        print("please update error mod manual" + "\n")
        print("list mod erroris in log file: logs.txt \n")
    if NOT_ERROR:
        logFile.write("All mod is updated\n list mod: \n")
        for mod in mods:
            mod_About = os.path.join(
                gameDir,
                "steamcmd",
                "steamapps",
                "workshop",
                "content",
                "294100",
                mod,
                "About",
                "About.xml",
            )
            openFile = open(mod_About, encoding="utf8").read()
            mod_name = openFile.split("</name>")[0].split("<name>")[1]
            logFile.write(mod + ": " + mod_name + "\n")
    for m in message:
        rawLogFile.write(m + "\n")
    logFile.close()
    rawLogFile.close()
    os.symlink(
        os.path.join(gameDir, "steamcmd", "steamapps", "workshop", "content", "294100"),
        os.path.join(gameDir, "LinkNeverDie.Com-GSE", "mods"),
    )


Handling()
