import pip
import sys
import subprocess

def main():
    install()
    import menus
    menus.main_menu()


def install():
    importlist = ["pygame", "pygame_menu", "tinydb"]

    print("Checking installations...")

    for lib in importlist:
        try:
            globals()[lib] = __import__(lib)
            print(f"{lib} currently installed")
        except ImportError as e:
            print("Error -> ", e)
            print("Installing ", lib)
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

if __name__ == "__main__":
    main()



