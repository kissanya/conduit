"""
A modul célja, hogy ne kelljen minden egyes példánál ismételni a megfelelő Chrome driver létrehozását.
Importálás után elég a get_preconfigured_chrome_driver() függvényt meghívni.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_preconfigured_chrome_driver() -> webdriver.Chrome:
    s = Service(executable_path=ChromeDriverManager().install())
    o = Options()
    o.add_experimental_option('detach', True)

    return webdriver.Chrome(service=s, options=o)


# Csak példa a funkció használatára.
# Más modulba importálva ez a rész nem fog lefutni.
if __name__ == '__main__':

    driver = get_preconfigured_chrome_driver()
    driver.get('https://www.progmasters.hu')

    driver.maximize_window()
