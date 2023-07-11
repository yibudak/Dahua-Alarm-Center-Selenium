# Dahua Alarm Center Selenium

## Overview
"Dahua-Alarm-Center-Selenium" is a Python script developed to automate the process of monitoring and logging alarms from the Dahua Alarm Center using Selenium WebDriver. The script is designed to log in to the Dahua Alarm Center, navigate to the alarm center, enable alarm tracking, fetch alarms, and print new alarms' data.

## Features
- Automatic login to Dahua Alarm Center
- Navigation to the Alarm Center page
- Enabling alarm tracking
- Fetching and displaying new alarms
- After fetching 50 alarms, it restarts the whole process to prevent memory overload.

## Installation
Clone the repository:

```
git clone https://github.com/yibudak/Dahua-Alarm-Center-Selenium.git
```

Change your directory:

```
cd Dahua-Alarm-Center-Selenium
```

Install the requirements:

```
python3 -m pip install -r requirements.txt
```

## Usage

You can run the script with required arguments: host, username, password, and camera-list.

Example:

```
python3 connector.py --host yourHost --username yourUsername --password yourPassword --camera-list cameraList.json --bot-token "BOT_TOKEN" --chat-id "CHAT_ID"
```

## Required Arguments

- **--host**: The host URL of the Dahua Alarm Center. (eg: 192.168.1.100)
- **--username**: The username used for login.
- **--password**: The password used for login.
- **--camera-list**: The list of cameras to monitor in JSON format.
- **--bot-token**: Telegram bot token.
- **--chat-id**: Telegram chat id where to send notifications.

## Dependencies

Firefox and geckodriver are required to run the script.

Make sure to install these dependencies before running the script.

## Notes

This project is a work in progress and subject to change. Please make sure to pull the latest changes from the master branch before use.

## Contributing
We appreciate all contributions. If you're planning to contribute back bug fixes or features, please file an issue describing what you're fixing or feature you're adding.

## License
This project is licensed under AGPL-3.0 License - see the [LICENSE](LICENSE) file for details.