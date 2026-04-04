from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time


def detect_glassdoor_apply(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        result = {
            "apply_type": "unknown",
            "external_url": None,
            "error": None,
        }

        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)

            selectors = [
                "a:has-text('Apply Now')",
                "button:has-text('Apply Now')",
                "a:has-text('Easy Apply')",
            ]

            button = None
            for sel in selectors:
                if page.locator(sel).count() > 0:
                    button = page.locator(sel).first
                    break

            if not button:
                result["error"] = "no_apply_button"
                return result

            original_url = page.url

            # popup
            try:
                with page.expect_popup(timeout=3000) as popup_info:
                    button.click()
                popup = popup_info.value
                popup.wait_for_load_state("domcontentloaded", timeout=5000)
                time.sleep(1)

                result["apply_type"] = "external_popup"
                result["external_url"] = popup.url
                return result

            except PlaywrightTimeoutError:
                pass

            # same tab
            button.click()
            page.wait_for_timeout(2000)

            if page.url != original_url:
                result["apply_type"] = "external_same_tab"
                result["external_url"] = page.url
                return result

            # modal
            if page.locator("[role='dialog']").count() > 0:
                result["apply_type"] = "glassdoor_easy_apply"

        except Exception as e:
            result["error"] = str(e)

        finally:
            browser.close()

        return result