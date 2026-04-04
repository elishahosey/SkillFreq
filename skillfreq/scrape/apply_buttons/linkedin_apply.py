from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time


APPLY_TEXTS = ["easy apply", "apply", "continue", "company website"]


def detect_linkedin_apply(url):

    
    print("URL TYPE:", type(url))
    print("URL VALUE:", url)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state="linkedin_state.json")
        page = context.new_page()

        result = {
            "apply_type": "unknown",
            "external_url": None,
            "error": None,
        }

        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(3000)
            
            if page.locator(".modal__overlay--visible").count() > 0:
                result["apply_type"] = "login_required"
                result["error"] = "signin_modal_still_present"
                return result

            # find button
            button = None
            buttons = page.locator("button, a")

            for i in range(buttons.count()):
                el = buttons.nth(i)
                try:
                    text = (el.inner_text(timeout=1000) or "").lower()
                    if any(t in text for t in APPLY_TEXTS):
                        button = el
                        break
                except:
                    continue

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
                result["apply_type"] = "easy_apply"
                return result

        except Exception as e:
            result["error"] = str(e)

        finally:
            browser.close()

        return result