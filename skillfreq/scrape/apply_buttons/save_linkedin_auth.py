from playwright.sync_api import sync_playwright


def save_linkedin_auth():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")
        input("After logging into LinkedIn in the browser, press Enter in this terminal...")

        context.storage_state(path="linkedin_state.json")
        browser.close()


if __name__ == "__main__":
    save_linkedin_auth()