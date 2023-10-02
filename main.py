# python -m pip install selenium webdriver-manager
import json
import configparser
import csv

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

config = configparser.ConfigParser()
config.read("res/Properties.ini")
user = config['DEFAULT']['user']
password = config['DEFAULT']['password']
filename = config['DEFAULT']['filename_data']
file_out = config['DEFAULT']['filename_out']


def toAletaCSV(fulldata):
    f = open('res/'+file_out, 'w+', newline='')
    writer = csv.writer(f)
    writer.writerow(["Sobrenom", "Altura Espatlles", "Altura Espatlles Relativa", "Altura", "Altura Relativa", "Email"])
    writer.writerows(fulldata)
    f.close()


def getCastellersInfo(ids, driver):
    castellers = []
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
        castellers.append([mote, espat, espat_rel, alt, alt_rel, email])
    return castellers


def scanCastellersIds():
    file = open("res/" + filename, "r")
    str_file = file.read()
    castellers_data = json.loads(str_file)
    #Read from fitxer list-ajax amb esquelet:
    #{
    #"data": [
    #    {
    #        "photo": "\u003Cimg src=\u0022https:\/\/app.fempinya.cat\/media\/avatars\/avatar.jpg\u0022 class=\u0022img-avatar img-avatar32\u0022 alt=\u0022\u0022\u003E",
    #        "name": String,
    #        "alias": String,
    #        "status": String,
    #        "tags": null,
    #        "gender": "\u003Cspan style=\u0022color: deeppink;\u0022 class=\u0022si si-symbol-female\u0022\u003E\u003C\/span\u003E",
    #        "birthdate": null,
    #        "position": String,
    #        "id_casteller": int
    #    },{...
    #    }],
    #    "recordsTotal": 696,
    #    "recordsFiltered": 696
    # }
    #
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
    ids = scanCastellersIds()   #Ids castellers
    full_info = getCastellersInfo(ids, driver)  #Informació completa castellers
    toAletaCSV(full_info)   #Convertir a CSV

    sleep(2)
    driver.quit()


if __name__ == '__main__':
    femPinya()
    print("\nNerviiiis!!!! Tremola més que el 2d7!! De res colla!!")
