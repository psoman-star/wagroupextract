
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# --- CONFIGURATION ---
CHROME_PROFILE_PATH = "/path/to/your/chrome/profile"  # e.g. "/Users/you/Library/Application Support/Google/Chrome/Default"
GROUP_NAME = "My WhatsApp Group"                       # exact group chat name
# ----------------------

def init_driver():
    opts = Options()
    opts.add_argument(f"--user-data-dir={CHROME_PROFILE_PATH}")
    # opts.add_argument("--headless")  # uncomment if you don't need to see the browser
    driver = webdriver.Chrome(options=opts)
    driver.get("https://web.whatsapp.com/")
    return driver

def wait_for_login(driver, timeout=60):
    # Wait until the chats panel has loaded (indicating that you're logged in)
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "pane-side"))
    )

def open_group_chat(driver, group_name):
    # Find the chat in the sidebar by title attribute
    chat = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, f"//span[@title='{group_name}']")
        )
    )
    chat.click()

def open_group_info(driver):
    # Click the group header to open info pane
    info_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//header//div[@role='button' and @title]")
        )
    )
    info_btn.click()

def extract_members(driver):
    # Wait for the participants pane to appear
    participants_pane = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@role='region' and .//span[text()='Participants']]")
        )
    )
    # Scroll pane to load all members
    for _ in range(5):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", participants_pane)
        time.sleep(0.5)

    # Each participant is inside a div with data-testid="cell-frame-container"
    elems = participants_pane.find_elements(By.XPATH,
        ".//div[@data-testid='cell-frame-container']")
    members = []
    for el in elems:
        # The name is in a span with dir="auto"
        name_span = el.find_element(By.XPATH, ".//span[@dir='auto']")
        members.append(name_span.text)
    return members

if __name__ == "__main__":
    driver = init_driver()
    print("Waiting for WhatsApp Web login (QR scan if needed)...")
    wait_for_login(driver)

    print(f"Opening group chat: {GROUP_NAME}")
    open_group_chat(driver, GROUP_NAME)

    print("Opening group info pane…")
    open_group_info(driver)

    print("Extracting members…")
    members = extract_members(driver)
    print(f"Found {len(members)} members:")
    for m in members:
        print(" -", m)

    driver.quit()
