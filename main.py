import os
import sys
import time
import requests
import subprocess

from version import VERSION


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
        result = os.system(f"notify-send '===========ULTRA_UPDATE===========' '{text}'")
        time.sleep(1)
    print_add(text=str("[Notification] " + text), text_list=text_list)


def check_text(text: str, check_list: list[str]) -> bool:
    for check in check_list:
        if check in text:
            return True
    return False


def main():
    all_lines = []
    print_add(
        f"\n\n\n========== Updating APPS today : {time.strftime('%Y-%m-%d %H:%M:%S')} ==========\n\n\n",
        all_lines,
    )

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
        "no longer supported"
        "using this runtime"
    ]

    n_apps = 1
    flag = 1
    if process.stdout:
        for line in process.stdout:
            if check_text(line, text_to_skip):
                continue
            if "Nothing to do." in line:
                notify("No apps to update.", all_lines)
                print_add(f"{line.strip()}", all_lines)
                break
            if "Updating " in line and flag:
                notify(f"{n_apps} apps are being updated.", all_lines)
                flag = 0
                n_apps -= 1
            elif str(n_apps) + ". " in line:
                print("------------------", n_apps, line)
                n_apps += 1
            print_add(f"{line.strip()}", all_lines)

    update_log = os.path.join(os.path.expanduser("~"), "update_log.txt")
    print(update_log)

    if os.path.exists(update_log):
        with open(update_log, "r") as f:
            current_lines = f.readlines()
    else:
        current_lines = []

    return_code = process.wait()

    if return_code != 0:
        print_add(f"Process failed with code: {return_code}")
    stop = time.perf_counter()
    print_add(
        f"{int(stop - start)//60} minutes" if int(stop - start) // 60 > 0 else "",
        all_lines,
        end="",
    )
    print_add(f" {int(stop - start) % 60} seconds.", all_lines)

    current_lines.extend(all_lines)
    with open(update_log, "w") as f:
        f.writelines(current_lines)

    notify(f"{n_apps} apps have been updated.", all_lines)


def check_update():
    url = "https://raw.githubusercontent.com/TLPotatoe/Ultra_Update/refs/heads/main/version.py"
    request = requests.get(url)
    if request.status_code == 200:
        if VERSION in request.content.decode("utf-8"):
            print("App is up to date.")
            return
        else:
            os.system(
                f"cd {os.path.dirname(__file__)} && git stash && git pull && python install.py && python main.py -no_check"
            )
            sys.exit()


if __name__ == "__main__":
    if not "-no_check" in sys.argv:
        check_update()
    main()
