import os
import subprocess
from Handling import *


""" Get all mod in folder """
mods = [
    name
    for name in os.listdir(ModRootFolder)
    if os.path.isdir(os.path.join(ModRootFolder, name))
]

""" update mod """


def update_mods(modslist):
    modUpdate = ""
    for mod in modslist:
        print("\nchecking mod: " + mod)
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
    unlink()
    message = update_mods(mods)
    modError = []
    NOT_ERROR = True
    if os.path.exists(os.path.join("UpdateMod", "logs.txt")):
        os.remove(os.path.join("UpdateMod", "logs.txt"))
    if os.path.exists(os.path.join("UpdateMod", "RawLogs.txt")):
        os.remove(os.path.join("UpdateMod", "RawLogs.txt"))
    if not os.path.exists(os.path.join(os.path.join("UpdateMod"))):
        os.mkdir(os.path.join("UpdateMod"))
    logFile = open(os.path.join("UpdateMod", "logs.txt"), "a")
    rawLogFile = open(os.path.join("UpdateMod", "RawLogs.txt"), "a")
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
        logFile.write("please update error mod manual or try again this app" + "\n")
        logFile.write("list mod error: \n")
        for mod in modError:
            logFile.write(mod + "\n")
        print("please update error mod manual" + "\n")
        print("list mod erroris in log file: logs.txt \n")
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
        Modfolder,
    )
    input("Press Enter to continue...")
