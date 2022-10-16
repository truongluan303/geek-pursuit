from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from config import CHROME_DRIVER_PATH
from config import FIREFOX_BIN
from config import FIREFOX_DRIVER_PATH
from config import GOOGLE_CHROME_BIN
from config import is_production
from config import WEB_DRIVER_TYPE


def soup_from_js_site(url) -> str:
    return BeautifulSoup(html_source_from_js_site(url), "html.parser")


def html_source_from_js_site(url) -> str:
    driver = generate_driver()
    driver.start_client()
    driver.get(url)
    htmlsrc = driver.page_source
    driver.quit()
    return htmlsrc


def generate_driver():
    if WEB_DRIVER_TYPE == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")

        binary = FirefoxBinary(*([FIREFOX_BIN] if is_production() else []))
        return webdriver.Firefox(
            firefox_binary=binary, executable_path=FIREFOX_DRIVER_PATH, options=options
        )
    if WEB_DRIVER_TYPE == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = GOOGLE_CHROME_BIN
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        return webdriver.Chrome(
            executable_path=CHROME_DRIVER_PATH, chrome_options=chrome_options
        )
    if WEB_DRIVER_TYPE == "edge":
        return webdriver.Edge()
    if WEB_DRIVER_TYPE == "safari":
        return webdriver.Safari()

    raise Exception(
        f"Unknown webdriver: `{WEB_DRIVER_TYPE}`. "
        "Currently only support `chrome`, `edge`, `safari`, or `firefox`."
    )
