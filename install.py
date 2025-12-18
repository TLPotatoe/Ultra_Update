import os

PROFILE = os.path.join(os.path.expanduser("~"), ".profile")
PATH = os.path.abspath("main.py")

def main():
    with open(PROFILE, "r") as f:
        lines = f.readlines()
    presence = [line for line in lines if PATH in line and 'python3' in line]
    if len(presence):
        # lines[lines.index(presence[0])] = f"python3 '{PATH}'\n"
        return
    else:
        lines.append(f"python3 '{PATH}'\n")
    with open(PROFILE, "w") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()