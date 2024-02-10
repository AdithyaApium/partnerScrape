from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

ciscoPartnersLink="https://locatr.cloudapps.cisco.com/WWChannels/LOCATR/pf/index.jsp#/"

def getPartnerList():
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(ciscoPartnersLink)
    wait=WebDriverWait(driver=driver,timeout=5)
    

getPartnerList()