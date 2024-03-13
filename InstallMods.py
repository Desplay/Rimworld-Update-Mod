from Handling import *
import subprocess

""" Get game directory """

unlink()


def Install_mods(modslist):
    modInstall = ""
    for mod in modslist:
        modInstall = modInstall + " +workshop_download_item 294100 " + mod
    print("start Install mod, all mod will be updating in one time, please wait...")
    messageInByte = subprocess.run(
        steamcmd + " +login anonymous" + modInstall + " +quit",
        capture_output=True,
        shell=True,
    ).stdout.splitlines()
    message = []
    for m in messageInByte:
        message.append(m.decode("utf-8"))
    return message


def Handling():
    mod_Input = input("Enter mod id: ")
    modsId = mod_Input.split(" ")
    message = Install_mods(modsId)
    modError = []
    NOT_ERROR = True
    if os.path.exists(os.path.join("InstallMod", "logs.txt")):
        os.remove(os.path.join("InstallMod", "logs.txt"))
    if os.path.exists(os.path.join("InstallMod", "RawLogs.txt")):
        os.remove(os.path.join("InstallMod", "lawLogs.txt"))
    if not os.path.exists(os.path.join(os.path.join("InstallMod"))):
        os.mkdir(os.path.join("InstallMod"))
    logFile = open(os.path.join("InstallMod", "logs.txt"), "a")
    rawLogFile = open(os.path.join("InstallMod", "lawLogs.txt"), "a")
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
        logFile.write("please install error mod manual or try again this app" + "\n")
        logFile.write("list mod error: \n")
        for mod in modError:
            logFile.write(mod + "\n")
        print("please install error mod manual" + "\n")
        print("list mod erroris in log file: logs.txt \n")
    logFile.write("All mod is installed\n list mod: \n")
    for mod in modsId:
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
