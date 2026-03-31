import subprocess
import uuid
import os

def get_result_image(name):
    filename = f"{name}_{uuid.uuid4().hex}.png"

    command = f"""
node -e "
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage();

  await page.goto('https://osama.noorayn.net/login.php');
  await page.getByPlaceholder('Enter your name').fill('{name}');
  await page.getByRole('button', {{ name: 'Login' }}).click();

  await page.waitForSelector('text=Hi {name}!');
  await page.getByRole('button', {{ name: 'Check Results' }}).click();

  await page.waitForTimeout(3000);
  await page.screenshot({{ path: '{filename}' }});

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