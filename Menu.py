from InstallMods import Handling as InstallMods
from UpdateMods import Handling as UpdateMods
from LinkFolderMod import Handling as LinkFolderMod

def Menu():
    print("1. Install Mods")
    print("2. Update Mods")
    print("3. Link Mods")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        InstallMods()
    elif choice == "2":
        UpdateMods()
    elif choice == "3":
        LinkFolderMod()
    elif choice == "4":
        exit()
    else:
        print("Invalid choice")
        Menu()
Menu()