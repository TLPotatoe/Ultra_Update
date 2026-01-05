import os

PROFILE = os.path.join(os.path.expanduser("~"), ".profile")
PATH = os.path.abspath("main.py")
COMMAND = f"python3 '{PATH}' &\n"

def main():
    print(f"cd {os.path.dirname(PATH)} && git pull")
    os.system(f"cd {os.path.dirname(PATH)} && git pull")
    with open(PROFILE, "r") as f:
        lines = f.readlines()
    presence = [line for line in lines if PATH in line and COMMAND in line]
    if len(presence):
        # lines[lines.index(presence[0])] = f"python3 '{PATH}'\n"
        return
    else:
        lines.append(COMMAND)
    with open(PROFILE, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
    print("Install done.")