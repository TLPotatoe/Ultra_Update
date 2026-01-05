import os

from main import check_user

PROFILE = os.path.join(os.path.expanduser("~"), ".profile")
PATH = os.path.dirname(__file__)
SETTINGS = os.path.join(PATH, "settings")
COMMAND = f"python3 '{os.path.join(PATH, 'main.py')}' &\n"


def main():
    print(f"cd {PATH} && git pull")
    os.system(f"cd {PATH} && git pull")
    os.system("python -m pip install -r requirements.txt")
    if os.path.exists(PROFILE):
        with open(PROFILE, "r") as f:
            lines = f.readlines()
    else:
        lines = []
    presence = [line for line in lines if PATH in line and COMMAND in line]
    if len(presence):
        pass
    else:
        lines.append(COMMAND)
    with open(PROFILE, "w") as f:
        f.writelines(lines)

    if not os.path.exists(SETTINGS):
        answer1 = check_user("Turn on auto Ultra_Update update on startup? [Y/n]")
        answer2 = check_user("Turn on auto Flatpak update on startup? [Y/n]")
        with open(SETTINGS, "w") as f:
            f.write(f"Ultra_update:{str(answer1)}\n")
            f.write(f"Flatpak_update:{str(answer2)}\n")


if __name__ == "__main__":
    main()
    print("Install done.")
