import os
import logging
import pathlib
import platform
import sys
import time

# suppress TensorFlow Lite logs (safe even if TF not used)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService

logging.basicConfig(
    format="[%(levelname)s] instagram-activities-wipe: %(message)s",
    level=logging.INFO
)

# -------------------- CONSTANTS --------------------
MODE = -1
LIKES_URL = "https://www.instagram.com/your_activity/interactions/likes"
COMMENTS_URL = "https://www.instagram.com/your_activity/interactions/comments"
REELS_URL = "https://www.instagram.com/your_activity/photos_and_videos/reels"
POSTS_URL = "https://www.instagram.com/your_activity/photos_and_videos/posts"

AT_ONCE_DELETE = 20

# -------------------- START --------------------
logging.info("Starting...")

try:
    # ChromeDriver service
    service = ChromeService(log_path=os.devnull)

    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")

    if platform.system() == "Windows":
        wd = pathlib.Path().absolute()
        options.add_argument(f"user-data-dir={wd}\\chrome-profile")
    else:
        options.add_argument("user-data-dir=chrome-profile")

    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1200, 900)
    logging.info("Opened Chrome browser")

    # -------------------- ASCII BANNER --------------------
    ascii_title = r"""
██╗███╗   ██╗ ███████╗ ████████╗  █████╗  ██████╗ ███████╗ ██╗
▓▓║▓▓▓▓╗  ▓▓║ ▓▓╔════╝ ╚══▓▓╔══╝ ▓▓╔══▓▓╗ ▓▓╔══▓▓╗▓▓╔════╝ ▓▓║
▒▒║▒▒╔▒▒╗ ▒▒║ ▒▒▒▒▒▒▒╗     ▒▒║    ▒▒▒▒▒▒▒║ ▒▒║  ▒▒║▒▒▒▒▒╗   ▒▒║
░░║░░║╚░░╗░░║ ╚════░░║     ░░║    ░░╔══░░║ ░░║  ░░║░░╔══╝   ░░║
  ║  ║  ╚════║ ░░░░░░░║     ║     ║  ║  ║ ░░░░░░╔╝░░░░░░░╗░░░░░░░╗
  ╚══╝  ╚════╝ ╚══════╝     ╚═╝    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝
"""
    print("\033[31m" + ascii_title + "\033[0m")

    # -------------------- MENU --------------------
    print("\n=== INSTAGRAM WIPE TOOL ===")
    print("1. Delete Comments")
    print("2. Delete Likes")
    print("3. Delete Reels")
    print("4. Delete Posts")

    while True:
        mode = input("Choose mode [1/2/3/4]: ").strip()
        if mode in {"1", "2", "3", "4"}:
            MODE = int(mode)
            break

    # -------------------- NAVIGATION --------------------
    if MODE == 1:
        driver.get(COMMENTS_URL)
        target_url = COMMENTS_URL
    elif MODE == 2:
        driver.get(LIKES_URL)
        target_url = LIKES_URL
    elif MODE == 3:
        driver.get(REELS_URL)
        target_url = REELS_URL
    else:
        driver.get(POSTS_URL)
        target_url = POSTS_URL

    logging.info(f"Opening {target_url}")

    # -------------------- LOGIN WAIT --------------------
    while True:
        if driver.current_url.startswith(target_url):
            logging.info("Login detected")
            break

        try:
            logging.info("Waiting for sign in... (log in manually)")
            wait = WebDriverWait(driver, 60)

            def is_not_now_present(drv):
                try:
                    btn = drv.find_element(By.CSS_SELECTOR, "div[role='button']")
                    return btn.text == "Not now"
                except Exception:
                    return False

            wait.until(is_not_now_present)
            driver.find_element(By.CSS_SELECTOR, "div[role='button']").send_keys(Keys.ENTER)
            logging.info("Clicked 'Not now'")
            break

        except TimeoutException:
            pass

    # -------------------- DELETION LOGIC --------------------
    def start_deletion():
        while True:
            logging.info("Waiting for items to load...")
            time.sleep(2)

            # Click Select
            select_clicked = False
            for el in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]'):
                if el.text == "Select":
                    if any(j.text == "No results" for j in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.Text"]')):
                        logging.info("No items found. Exiting.")
                        return
                    driver.execute_script("arguments[0].click();", el)
                    select_clicked = True
                    break

            if not select_clicked:
                logging.info("Nothing selectable. Exiting.")
                return

            # Select items
            selected = 0
            time.sleep(1)
            icons = driver.find_elements(By.CSS_SELECTOR, 'div[data-bloks-name="ig.components.Icon"]')

            for icon in icons:
                style = icon.get_attribute("style") or ""
                if "circle__outline" in style:
                    driver.execute_script("arguments[0].click();", icon)
                    selected += 1
                    logging.info(f"Selected item ({selected})")
                    if selected >= AT_ONCE_DELETE:
                        break

            if selected == 0:
                logging.info("No items selected. Exiting.")
                return

            # Click Delete / Unlike
            delete_text = "Delete" if MODE in (1, 3, 4) else "Unlike"
            for span in driver.find_elements(By.CSS_SELECTOR, 'span[data-bloks-name="bk.components.TextSpan"]'):
                if span.text == delete_text:
                    driver.execute_script("arguments[0].click();", span)
                    break
            else:
                logging.warning("Delete button not found. Refreshing...")
                driver.refresh()
                continue

            # Confirm dialog
            time.sleep(1)
            for btn in driver.find_elements(By.CSS_SELECTOR, 'div[role="dialog"] button'):
                try:
                    text = btn.find_element(By.CSS_SELECTOR, "div").text
                except Exception:
                    continue

                if text == delete_text:
                    driver.execute_script("arguments[0].click();", btn)
                    logging.info("Deletion confirmed")
                    break
                elif text == "OK":
                    driver.execute_script("arguments[0].click();", btn)
                    logging.warning("Rate limit hit. Refreshing...")
                    driver.refresh()
                    time.sleep(2)
                    break

    # -------------------- RUN --------------------
    start_deletion()

except KeyboardInterrupt:
    logging.info("Interrupted by user.")
    driver.quit()
    sys.exit(0)

except NoSuchWindowException:
    logging.exception("Browser window closed unexpectedly.")
    sys.exit(1)

except Exception:
    logging.exception("Unexpected error occurred.")
    sys.exit(1)