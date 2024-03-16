from Handling import *
import os

def Handling():
    os.symlink(
    os.path.join(gameDir, "steamcmd", "steamapps", "workshop", "content", "294100"),
    Modfolder,
    )