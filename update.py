import os
import sys
import subprocess
import time

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
    text_list.append(text + "\n")
    print(text, end=end)


def main():
    all_lines = []
    
    print_add(f"\n\n\n========== Updating APPS today : {time.strftime('%Y-%m-%d %H:%M:%S')} ==========\n\n\n", all_lines)
    command = "flatpak update -y"
    
    print_add(f"Running '{command}'", all_lines)    
    start = time.perf_counter()
    process = run_subp(command)
    
    n_apps = 0
    if process.stdout:
        for line in process.stdout:
            if '/' in line and '…' in line:
                n_apps = int(line[line.index('/') + 1 : line.index('…')])
            print_add(f"[{time.strftime('%H:%M:%S')}] {line.strip()}", all_lines)
    
    update_log = os.path.join(os.path.expanduser("~"), "update_log.txt")
    
    if os.path.exists(update_log):   
        with open(update_log, "r") as f:
            current_lines = f.readlines()
    else:
        current_lines = []

    return_code = process.wait()

    if return_code != 0:
        print_add(f"Process failed with code: {return_code}")
    stop = time.perf_counter()
    print_add(f"{int(stop - start)//60} minutes" if int(stop - start)//60 > 0 else "", all_lines, end="")
    print_add(f" {int(stop - start) % 60} seconds.", all_lines)
    
    current_lines.extend(all_lines)
    with open(update_log, "w") as f:
        f.writelines(current_lines)
    
    time.sleep(5)

    os.system(f"notify-send '===========ULTRA_UPDATE===========' '{n_apps} apps have been updated this time.'")

if __name__ == "__main__":
    main()