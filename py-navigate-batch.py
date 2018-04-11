"""
    Open Chrome browser to navigate a batch of websites.
"""

import time
import asyncio

from sys import (
    platform as _platform
)

from selenium import (
    webdriver,
)

from selenium.common.exceptions import (
    TimeoutException
)

from selenium.webdriver.support.ui import (
    WebDriverWait
)

from selenium.webdriver.support import (
    expected_conditions as EC
)

from batch import (
    batch1, batch2
)


async def chrome_navigate(driver_path, mini_batch=None):
    if mini_batch is None:
        return

    driver = webdriver.Chrome(driver_path)

    for x in mini_batch:
        driver.get(x["url"])
        try:
            # we have to wait for the page to refresh, the last thing that seems to be updated is the title
            WebDriverWait(driver, 10).until(EC.title_contains(x["title"]))
            print(driver.title)
            time.sleep(3)
        except TimeoutException:
            print("Timeout while navigating website")
            assert (1 == 0)

    driver.quit()


def test():
    driver_path = "browser/driver/chrome/{}/chromedriver{}"

    if _platform.startswith('linux'):
        driver_path = driver_path.format("linux64", "")
    elif _platform.startswith('darwin'):
        driver_path = driver_path.format("mac64", "")
    else:
        driver_path = driver_path.format("win32", ".exe")

    print(driver_path)

    b1 = asyncio.ensure_future(chrome_navigate(driver_path, batch1.SITES))
    b2 = asyncio.ensure_future(chrome_navigate(driver_path, batch2.SITES))

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(b1, b2))
    finally:
        loop.close()


if __name__ == "__main__":
    test()
