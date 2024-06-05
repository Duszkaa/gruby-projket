from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = options, service=ChromeService(r"C:\Users\Informatyka\Desktop\Testy\chromedriver-win64\chromedriver.exe"))

driver.get("http://6187az.pythonanywhere.com")

# dodawanie elementu
driver.find_element(By.ID, "NBadd").click()
driver.find_element(By.ID, "fCzynnosc").send_keys("Diegorinio")
driver.find_element(By.ID, "fOpis").send_keys("wita w strefie linuxa, tylko twardzi linuxiarze, distro lecace z nieba")
Select(driver.find_element(By.ID, "fPriorytet")).select_by_index(1)
driver.find_element(By.ID, "fData").send_keys("06062000")
driver.find_element(By.ID, "fGodzina").send_keys("12:30")
driver.find_element(By.ID, "sendButton").click()
time.sleep(1)

#edycja elementu
driver.find_element(By.ID, "btnUpdate1").click()
driver.find_element(By.ID, "fCzynnosc").clear()
driver.find_element(By.ID, "fCzynnosc").send_keys("Tomek")
driver.find_element(By.ID, "fOpis").clear()
driver.find_element(By.ID, "fOpis").send_keys("Tomek jednak wyszedl z strzefy linuxa")
Select(driver.find_element(By.ID, "fPriorytet")).select_by_index(0)
driver.find_element(By.ID, "fData").send_keys("08012022")
driver.find_element(By.ID, "fGodzina").send_keys("21:37")
driver.find_element(By.ID, "sendButton").click()
time.sleep(1)

#usuwanie elementu
driver.find_element(By.ID, "btnDelete1").click()
time.sleep(1)
Alert(driver).accept()


