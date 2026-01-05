import os

PROFILE = os.path.join(os.path.expanduser("~"), ".profile")
PATH = os.path.abspath("main.py")
COMMAND = f"python3 '{PATH}' &\n"


def main():
    print(f"cd {os.path.dirname(PATH)} && git pull")
    os.system(f"cd {os.path.dirname(PATH)} && git pull")
    os.system("python -m pip install -r requirements.txt")
    if os.path.exists(PROFILE):
        with open(PROFILE, "r") as f:
            lines = f.readlines()
    else:
        lines = []
    presence = [line for line in lines if PATH in line and COMMAND in line]
    if len(presence):
        return
    else:
        lines.append(COMMAND)
    with open(PROFILE, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
    print("Install done.")
