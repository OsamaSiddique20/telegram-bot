import subprocess
import uuid
import os

def take_screenshot(url):
    filename = f"{uuid.uuid4().hex}.png"

    # ensure url has protocol
    if not url.startswith("http"):
        url = "https://" + url

    command = f"""
node -e "
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage();

  await page.goto('{url}', {{ waitUntil: 'domcontentloaded' }});
  await page.waitForTimeout(3000);

  await page.screenshot({{ path: '{filename}', fullPage: true }});

  await browser.close();
}})();
"
"""

    subprocess.run(command, shell=True)

    return filename


def cleanup_file(path):
    try:
        os.remove(path)
    except Exception as e:
        print("Cleanup error:", e)