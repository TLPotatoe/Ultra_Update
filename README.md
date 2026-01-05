# Ultra_Update

Ultra_Update is a Python script that automates the process of updating your Flatpak applications on Linux. It runs in the background, checks for updates, and applies them automatically, ensuring your applications are always up-to-date. The script can also update itself.

## Features

-   **Automatic Flatpak Updates:** Runs `flatpak update -y` automatically.
-   **Automatic Self-Update:** Can automatically download and install new versions of itself from GitHub.
-   **Desktop Notifications:** Sends desktop notifications about the update status using `notify-send`.
-   **Startup Execution:** The script is configured to run automatically on system startup.
-   **Logging:** Keeps a log of all update activities in `~/update_log.txt`.
-   **Configurable:** You can configure the auto-update behavior during installation.

## How It Works

During installation, a command to run Ultra_Update is added to your `~/.profile` file. This makes the script run automatically every time you log in. When executed, it checks for Flatpak updates and for new versions of itself. You can enable or disable automatic updates for both Flatpak and Ultra_Update itself.

## Installation

1.  **Prerequisites:** Before installing, make sure you have the following dependencies installed:
    *   `python3`
    *   `git`
    *   `flatpak`
    *   A desktop environment that supports `notify-send` (e.g., GNOME, KDE, XFCE).

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/TLPotatoe/Ultra_Update.git
    cd Ultra_Update
    ```

3.  **Run the installer:**
    ```bash
    python3 install.py
    ```
    or
    ```bash
    ./install.sh
    ```
    The installer will prompt you to enable or disable automatic updates.

## Usage

Once installed, Ultra_Update will run automatically in the background. You can monitor its activity by checking the log file:

```bash
cat ~/update_log.txt
```

To change the settings after installation, you can edit the `settings` file in the project directory.

## Uninstallation

To uninstall Ultra_Update, follow these steps:

1.  **Remove the startup entry:**
    Open your `~/.profile` file and remove the line that looks like this:
    ```
    python3 '/path/to/your/Ultra_Update/main.py' &
    ```

2.  **Delete the project directory:**
    ```bash
    rm -rf /path/to/Ultra_Update
    ```
    (Replace `/path/to/Ultra_Update` with the actual path to the directory).


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.