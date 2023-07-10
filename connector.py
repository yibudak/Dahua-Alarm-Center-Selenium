from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import argparse
import json
import time
import httpx

"""
Yiğit Budak (https://github.com/yibudak/Dahua-Alarm-Center-Selenium)
Dahua Alarm Center Telegram Connector
"""

UserAgent = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"
)
options = Options()
# Dahua Alarm Center only works with Internet Explorer
options.set_preference(
    "general.useragent.override",
    UserAgent,
)


def load_camera_list(camera_list):
    """Load Camera List"""
    try:
        loaded_camera_list = json.loads(camera_list)
    except Exception as e:
        print("Loading Camera List Failed. Error:\n %s" % str(e))
        exit()
    return loaded_camera_list


def login(host, browser, username, password):
    """Login to Dahua Alarm Center"""
    browser.get(f"http://{host}")
    try:
        # Username
        username_field = browser.find_element(By.XPATH, "//input[@id='username']")
        username_field.clear()
        username_field.send_keys(username)
        # Password
        password_field = browser.find_element(By.XPATH, "//input[@id='password']")
        password_field.clear()
        password_field.send_keys(password)
        # Login
        login_button = browser.find_element(By.XPATH, "//a[@id='ulgin']")
        login_button.click()
        time.sleep(3)
    except Exception as e:
        print("Login Failed. Error:\n %s" % str(e))
        browser.close()
        exit()
    return True


def navigate_to_alarm_center(browser):
    """Navigate to Alarm Center"""
    try:
        # Alarm Center
        alarm_center_button = browser.find_element(By.XPATH, "//a[@id='xbjsz']")
        alarm_center_button.click()
        time.sleep(3)
    except Exception as e:
        print("Navigation to Alarm Center Failed. Error:\n %s" % str(e))
        browser.close()
        exit()
    return True


def enable_alarm_tracking(browser):
    """Enable Alarm Tracking"""
    try:
        # Alarm Tracking
        alarm_tracking_button = browser.find_element(
            By.XPATH, "//input[@id='alarmType_1']"
        )
        alarm_tracking_button.click()
        time.sleep(1)
    except Exception as e:
        print("Enable Alarm Tracking Failed. Error:\n %s" % str(e))
        browser.close()
        exit()
    return True


def check_session_status(browser):
    """
    Check Session Status
    :param browser: selenium.webdriver
    :return: Boolean
    """
    data = {
        "method": "global.keepAlive",
        "params": {"timeout": 300, "active": True},
        "session": None,
        "id": 100,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": UserAgent,
        "X-Request": "JSON",
        "X-Requested-With": "XMLHttpRequest",
    }

    cookies = {cookie["name"]: cookie["value"] for cookie in browser.get_cookies()}
    data["session"] = cookies["DhWebClientSessionID"]
    try:
        resp = httpx.post(
            f"{browser.current_url}RPC2",
            cookies=cookies,
            json=data,
            timeout=5,
            headers=headers,
            verify=False,  # Ignore SSL
        )
        resp.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"HTTP Error: {exc}")
        return False
    return resp.status_code == 200


def fetch_alarms(camera_list, browser):
    """Fetch Alarms"""

    found_signals = {}
    alarm_frame = browser.find_element(By.XPATH, "//iframe[@id='alarm_frame']")
    browser.switch_to.frame(alarm_frame)
    iteration = 0

    while True:
        # Check session status every 10 iterations
        if iteration % 10 == 0 and not check_session_status(browser):
            # If session is expired, restart the whole process
            return False

        signals = browser.find_elements(By.XPATH, "//div")
        for signal in signals:
            splitted_text = signal.text.split("\n")
            if len(splitted_text) == 4 and splitted_text[0] not in found_signals:
                camera_name = camera_list.get(splitted_text[3], False)
                data = {
                    "date": splitted_text[1],
                    "alarm_type": splitted_text[2],
                    "camera_name": camera_name or splitted_text[3],
                }
                found_signals[splitted_text[0]] = data
                # TODO: Send the data to Telegram
                print(f"New Alarm: {data}")

        if len(found_signals) >= 50:
            # If there are more than 50 alarms, restart the whole process
            return True

        time.sleep(3)  # Slow down the loop to avoid overloading the server
        iteration += 1


def main(host, username, password, camera_list):
    # Load the items
    try:
        json_file = open(camera_list, "r")
        loaded_camera_list = json.load(json_file)
    except FileNotFoundError:
        print("Camera List File Not Found")
        exit()

    # Open the browser
    driver = webdriver.Firefox(options=options)

    # Methods
    while True:
        # After reaching 50 signals, we start a new session,
        # thus avoiding memory bloat.
        login(host, driver, username, password)
        navigate_to_alarm_center(driver)
        enable_alarm_tracking(driver)
        fetch_alarms(camera_list=loaded_camera_list, browser=driver)
        time.sleep(3)  # Slow down the loop to avoid overloading the server


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Dahua Alarm Center Telegram Connector"
    )
    parser.add_argument(
        "--host",
        type=str,
        help="Host URL",
        required=True,
    )
    parser.add_argument(
        "--username",
        type=str,
        help="Username for login",
        required=True,
    )
    parser.add_argument(
        "--password",
        type=str,
        help="Password for login",
        required=True,
    )
    parser.add_argument(
        "--camera-list",
        type=str,
        help="List of cameras to monitor (JSON)",
        required=True,
    )
    args = parser.parse_args()
    main(args.host, args.username, args.password, args.camera_list)
