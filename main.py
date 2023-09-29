# python -m pip install selenium webdriver-manager
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

user = ""
password = ""
filename = "castellers_data.txt"


def getCastellersInfo(ids, driver):
    for i in ids:
        url = 'https://app.fempinya.cat/castellers/edit/' + str(i)
        driver.get(url)
        alt = driver.find_element(By.XPATH, "//input[contains(@id,'height')]").get_attribute("value")
        alt_rel = driver.find_element(By.XPATH, "//input[contains(@id,'relative_height')]").get_attribute("value")
        mote = driver.find_element(By.XPATH, "//input[contains(@id,'alias')]").get_attribute("value")
        espat = driver.find_element(By.XPATH, "//input[contains(@id,'shoulder_height')]").get_attribute("value")
        espat_rel = (driver.find_element(By.XPATH, "//input[contains(@id,'relative_shoulder_height')]")
                     .get_attribute("value"))
        try:
            email = (driver.find_element(By.XPATH, "//div[contains(@class,'col-sm-10 font-weight-lighter text-right')]")
                     ).text
        except NoSuchElementException:
            email = ""
        print(mote + ":\t", alt, "(Altura)\t", alt_rel, "(Altura relativa)\t", espat, "(Espatlla)\t", espat_rel,
              "(Espatlla relativa)\t", email, "(Email).")


def scanCastellersIds():
    file = open("res/" + filename, "r")
    str_file = file.read()
    castellers_data = json.loads(str_file)

    ids = []
    for casteller in castellers_data["data"]:
        ids.append(casteller["id_casteller"])
    return ids


def logIn(drive):
    usr = drive.find_element(By.XPATH, "//input[contains(@id,'email')]").send_keys(user)
    psw = drive.find_element(By.XPATH, "//input[contains(@id,'password')]").send_keys(password)
    smt = drive.find_element(By.XPATH, "//button[contains(@type,'submit')]").submit()


def femPinya():
    # instantiate options
    options = webdriver.ChromeOptions()
    # run browser in headless mode
    options.headless = True

    # instantiate driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    # load website
    url = 'https://app.fempinya.cat/'
    driver.get(url)

    logIn(driver)
    ids = scanCastellersIds()
    getCastellersInfo(ids[:100], driver)
    sleep(5)
    driver.quit()


if __name__ == '__main__':
    femPinya()
    print("\nNerviiiis!!!! Tremola més que el 2d7!! De res colla!!")
