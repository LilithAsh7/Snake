import sys
import subprocess


# Installs necessary modules and starts the main menu
def main():
    install()
    import menus
    menus.main_menu()


# Checks for modules and installs them if not present
def install():
    import_list = ["pygame", "pygame_menu", "tinydb"]

    print("Checking installations...")

    for lib in import_list:
        try:
            globals()[lib] = __import__(lib)
            print(f"{lib} currently installed")
        except ImportError:
            print("Installing ", lib)
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", lib])


if __name__ == "__main__":
    main()
