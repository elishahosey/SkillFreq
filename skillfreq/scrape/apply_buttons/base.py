from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError



def fetch_rendered_html(url: str) -> str:
    """
    Fetch fully rendered HTML using Playwright.
    Designed for JS-heavy sites (Oracle, Workday, LinkedIn, etc.)
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded")

            # let JS boot (Oracle pages need this)
            page.wait_for_timeout(3000)

            # Try to wait for meaningful content instead of skeleton HTML
            selectors = [
                "[data-automation-id='jobDescription']",
                "[data-automation-id='job-description']",
                "article",
                "main",
                "section"
            ]

            found = False

            for sel in selectors:
                try:
                    page.locator(sel).first.wait_for(timeout=4000)
                    found = True
                    break
                except PlaywrightTimeoutError:
                    continue

            # fallback: wait for network idle (sometimes helps)
            if not found:
                try:
                    page.wait_for_load_state("networkidle", timeout=5000)
                except:
                    pass

            # final buffer (important for Oracle)
            page.wait_for_timeout(2000)

            html = page.content()
            return html

        except Exception as e:
            print(f"[fetch_rendered_html] error: {e}")
            return ""

        finally:
            browser.close()
