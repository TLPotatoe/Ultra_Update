import os
import sys
import time
import requests
import subprocess

from version import VERSION

PATH = os.path.dirname(__file__)
SVG = os.path.join(PATH, "ultra_update.svg")
SETTINGS = os.path.join(PATH, "settings")


def get_setting(name: str) -> bool:
    if os.path.exists(SETTINGS):
        with open(SETTINGS, "r") as f:
            lines = f.readlines()
        for line in lines:
            if name in line:
                if "true" in line[line.find(":") + 1 :].lower():
                    return True
                else:
                    return False
    return False


def check_user(text: str, default: bool = True):
    answer = input(text).lower().strip()
    if answer == "":
        return default
    if answer == "y":
        return True
    else:
        return False


def run_subp(command: str, cwd: str = None) -> subprocess.Popen:
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd,
        bufsize=1,
    )
    return process


def print_add(text: str, text_list: list, end: str = "\n") -> None:
    text_list.append(f"[{time.strftime('%H:%M:%S')}] " + text + "\n")
    print(text, end=end)


def notify(text: str, text_list: list[str]) -> None:
    result = -1
    while result:
        result = os.system(f"notify-send -i {SVG} '==ULTRA_UPDATE==' '{text}'")
        time.sleep(5)
    print_add(text=str("[Notification] " + text), text_list=text_list)


def check_text(text: str, check_list: list[str]) -> bool:
    for check in check_list:
        if check in text:
            return True
    return False


def write_log(text: list[str]):
    update_log = os.path.join(os.path.expanduser("~"), "update_log.txt")
    if os.path.exists(update_log):
        with open(update_log, "r") as f:
            current_lines = f.readlines()
    else:
        current_lines = []

    # text.append("\nEnd of log.\n")
    current_lines.extend(text)
    with open(update_log, "w") as f:
        f.writelines(current_lines)


def check_update():
    all_lines = []
    url = "https://raw.githubusercontent.com/TLPotatoe/Ultra_Update/refs/heads/main/version.py"
    command = f"cd {os.path.dirname(__file__)} && git pull && python install.py && python main.py -only_apps -front"
    request = requests.get(url)
    print_add("\n\n\nChecking Ultra_Update version...", all_lines)
    if request.status_code == 200:
        content = request.content.decode("utf-8")
        version = content[content.find('"') + 1 : content.rfind('"')]
        print_add(f"Current:{VERSION}. Online:{version}", all_lines)
        if VERSION > version:
            print_add("You're ahead!", all_lines)
            write_log(all_lines)
            return 0
        elif VERSION < version:
            print_add(f"Newer version found: {version}\n", all_lines)
            if not get_setting("Ultra_update"):
                if not "-front" in sys.argv:
                    os.system(f"gnome-terminal -- bash -c 'python {__file__} -front'")
                    write_log(all_lines)
                    return 1
                if check_user(f"Update Ultra_Update to {version}? [Y/n]"):
                    os.system(command)
                    write_log(all_lines)
                    return 1
            else:
                print_add("Auto updating.", all_lines)
                os.system(command)
            write_log(all_lines)
        elif VERSION == version:
            print_add("App is up to date.", all_lines)
            write_log(all_lines)
            return 0
    else:
        print_add(f"Bad request status: {request.status_code}")
        write_log(all_lines)
        return 0
    return 0


def update_apps():
    all_lines = []
    if not get_setting("Flatpak_update"):
        if not "-front" in sys.argv:
            os.system(
                f"gnome-terminal -- bash -c 'python {__file__} -front -only_apps'"
            )
            return
        if not check_user("Would you like to update apps? [Y/n]"):
            return
    else:
        print_add("Auto update on.\n", all_lines)
    print_add(
        f"\n========== Updating Apps at this date : {time.strftime('%Y-%m-%d %H:%M:%S')} ==========\n",
        all_lines,
    )
    print_add(f"Version:{VERSION}", all_lines)

    command = "flatpak update -y"

    print_add(f"Running '{command}'\n", all_lines)
    start = time.perf_counter()
    process = run_subp(command)

    text_to_skip = [
        "end-of-life",
        "recommend moving",
        "discontinued",
        "maintained",
        "security updates",
        "no longer supported" "using this runtime",
    ]

    n_apps = 0
    flag = 1
    if process.stdout:
        for line in process.stdout:
            if check_text(line, text_to_skip) or (
                len(line.split()) != 2 and "…" in line
            ):
                continue
            if "Nothing to do." in line:
                notify("No apps to update.", all_lines)
                print_add(f"{line.strip()}", all_lines)
                break
            if "Updating " in line and flag:
                notify(f"{n_apps} apps are being updated.", all_lines)
                flag = 0
            elif len(line.split()):
                if str(n_apps + 1) + "." in line.split()[0]:
                    n_apps += 1
            print_add(f"{line.strip()}", all_lines)

    return_code = process.wait()
    # cache cleaning
    print_add("Checking app cache", all_lines)
    process = run_subp("du -sh ~/.var/app/*/cache")
    for line in process.stdout:
        print_add(line, all_lines)

    process = run_subp("du -ch ~/.var/app/*/cache | tail -n 1")
    for line in process.stdout:
        print_add(line, all_lines)

    os.system("rm -rf ~/.var/app/*/cache")

    if return_code != 0:
        print_add(f"Process failed with code: {return_code}")
    stop = time.perf_counter()
    print_add(
        f"{int(stop - start)//60} minutes" if int(stop - start) // 60 > 0 else "",
        all_lines,
        end="",
    )
    print_add(f" {int(stop - start) % 60} seconds.", all_lines)
    write_log(all_lines)
    if n_apps:
        notify(f"{n_apps} apps have been updated.", all_lines)


def main():
    if not "-only_apps" in sys.argv:
        if check_update():
            sys.exit()
    update_apps()


if __name__ == "__main__":
    main()
