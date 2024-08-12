import math
import time
import os
from os import sys
import re
INSTALL_OPTIONS = ["A","S","N"]
PROGRAM_NAME = "\033[95mPyLib\033[0m"
## /\/\ end of imports /\/\

def read_file(filename):
    import_lines = []
    with open(filename, "r") as file_info:
        for line in file_info:
            if re.search(r'\bimport\b', line.lower()):
                import_lines.append(line.strip())
    return import_lines

def distinguish_imports(import_lines):
    libraries = []
    for statement in import_lines:
        parts = statement.split()
        if "import" in parts:
            if "from" in parts:
                from_index = parts.index("from")
                # The module name to import is right after 'from'
                libraries.append(parts[from_index + 1].split('.')[0])
                import_index = parts.index("import")
                for part in parts[import_index + 1:]:
                    if 'as' in part:
                        break
                    libraries.extend([p.split('.')[0] for p in part.split(',')])
            else:
                import_index = parts.index("import")
                for part in parts[import_index + 1:]:
                    if 'as' in part:
                        break
                    libraries.extend([p.split('.')[0] for p in part.split(',')])
    return list(set(libraries))  # Use set to remove duplicates


def check_libs(libraries):
    libs_stat = {}
    for library in libraries:
        try:
            __import__(library)
            libs_stat[library] = "GOOD"
        except ImportError:
            libs_stat[library] = "BAD"
    return libs_stat

def prompt_info(libs_stat):
    libs_not_installed = []
    counter = 0
    for lib in libs_stat:
        if libs_stat[lib] == "BAD":
            libs_not_installed.append(lib)
            counter += 1
    if libs_not_installed:
        print(f"\033[91mLibraries Not Installed!\033[0m; Libraries {counter}\n")
        for lib_name in libs_not_installed:
            print(f"Libraries Not Installed: {lib_name}")
        print("")
        install_prompt = "Install:   [A]ll   [S]elect    [N]one\n> "
        prompt = True
        install_option = None  # Initialize with a default value
        while prompt:
            install_option = input(install_prompt)
            if install_option.upper() not in INSTALL_OPTIONS:
                print("\033[91mPlease Choose A Valid Option\033[0m")
                prompt = True
            else:
                prompt = False
    else:
        install_option = "n"  # Default to 'n' if no libraries are missing
        print("\033[91mInstall Aborted\033[0m\n")
    return install_option.lower(), libs_not_installed

def choose_install(libs):
    counter = 0
    libs_install = {}
    to_exclude = []
    print("\nPlease Add The Number Of Library You Would Like To Exclude\nAdd a comma after every number or Q to add quit (ex: 1,2,3...):\n")
    for lib in libs:
        counter += 1
        libs_install[counter] = lib
        print(f" {counter} | {lib}")
    exclude = input("> ")
    if exclude.lower() == "q":
        return to_exclude
    else:
        exclude = exclude.split(",")
        for numbers in exclude:
            to_exclude.append(libs_install[int(numbers)])
        return to_exclude

def install_libs(libraries):
    print("\nPlease Confirm Libraries To Install\n")
    counter = 0
    for lib in libraries:
        counter +=1
        print(f" -> \033[92m {lib}\033[0m")
    print("")
    install_conf = input(f"Install {counter} Libraries? (y/n)\n> ")
    count = 0
    if install_conf.lower() == "y":
        start = time.time()
        for lib in libraries:
            count += 1
            os.system(f"pip install {lib}")
        end = time.time()
        print(f"\n\n\033[92mProcess' Finished; Took {round(end-start,2)} sec \033[0m\nThanks For Using {PROGRAM_NAME}")
        return True,count
    else:
        print("\033[91mInstall Aborted\033[0m\n")
        return False,count

def help_menu():
    print("\nWelcome To PyLib, Your Shortcut For Python Installs!\n")
    print("USAGE: \n python pylib.py <arg>\n -----------------------\n\n -?           Help Menu\n FILENAME     Test The Playlist")
    print("\n\033[91mIMPORTANT\033[0m\n Make sure if the Python file imports classes from a local file\n The file exists in the same dir as the current Python file!\n")

def main():
    if len(sys.argv) < 2:
        print("\033[91mFatal Error! ->\033[0mPlease Enter A Filename")
        exit()
    elif sys.argv[1] == "-?":
        help_menu()
        exit()
    else:
        filename = sys.argv[1]
        import_lines = read_file(filename)
        found_libraries = (distinguish_imports(import_lines))
        libs_stat = check_libs(found_libraries)
        install, libs_not_installed = prompt_info(libs_stat)
        if install == "a":
            install_libs(libs_not_installed)
        elif install == "s":
            selective_libs = choose_install(libs_not_installed)
            install_libs(selective_libs)
        elif install == "n":
            print("Install was either aborted, or nothing to install")


if __name__ == "__main__":
    main()
