from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from GSheets.updateSheet import writeNewData

from classes.partnerData import Partner
from classes.partnerData import Partner

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

gPartnerLink="https://cloud.google.com/find-a-partner/"

global lastVisitedIndex
lastVisitedIndex=-1

def getPartnerList():
    global lastVisitedIndex
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(gPartnerLink)
    wait=WebDriverWait(driver=driver,timeout=10)
    currentCardCount=0

    while True:
        wait.until(lambda driver:(len(driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']")))>currentCardCount)
        cardCount=len(driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']"))
        print("Card count updated from ",currentCardCount," to ",cardCount)
        if((not cardCount>currentCardCount)):
            break
        currentCardCount=cardCount
        print("Found cards",cardCount," - ",currentCardCount)

        
        for ind in range(lastVisitedIndex+1,cardCount):
            # if(ind<=2193):
            #     lastVisitedIndex=ind
            #     continue
            loadedCards=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"a[data-test-id='partner-link']")))
            print("Starting from partner ",ind+1)
            try:
                partner=Partner()
                partner.source="Google"
                loadedCards[ind].click()
            except:
                print("Error clicking card ",ind+1)

            # Wait for everythinf to be loaded
            # try:
            skeletons=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"cs-skeleton")))
            while len(skeletons)>0:
                # wait.until(EC.staleness_of(skeletons[0]))
                skeletons=driver.find_elements(By.CSS_SELECTOR,"cs-skeleton")
            # except:
            #     print("Error waiting for skeletons")

            try:
                
                # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"app-contact-icons>h2")))
            
                contactDetails=driver.find_elements(By.CSS_SELECTOR,"h2[title='Contact Details']")
                if(len(contactDetails)>0):
                    websiteElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner website']")
                    if(len(websiteElement)>0):
                        partner.contactDetails.web=websiteElement[0].get_attribute("href")
                    emailElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner email address']")
                    if(len(emailElement)>0):
                        partner.contactDetails.email=emailElement[0].get_attribute("href").split("mailto:")[1]
                    phoneElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner phone number']")
                    if(len(phoneElement)>0):
                        partner.contactDetails.phone=phoneElement[0].get_attribute("href").split("tel:")[1]
                
            except:
                print("No contact info")


            try:
                # nameElement=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1[data-test-id='title']")))
                nameElement=driver.find_element(By.CSS_SELECTOR,"h1[data-test-id='title']")
                partner.name=nameElement.text
            except:
                print("No name in partner ",ind+1)

            try:
                # specContainer=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"p[data-test-id='specializations-data']")))
                specContainer=driver.find_element(By.CSS_SELECTOR,"p[data-test-id='specializations-data']")
                partner.specializations=specContainer.text.split(",")
            except:
                print("No specs in partner ",ind+1)

            try:
                locationListContainer=driver.find_element(By.CSS_SELECTOR,"div.detail-locations")
                # locationListContainer=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.detail-locations")))
                countryElements=locationListContainer.find_elements(By.CSS_SELECTOR,"app-location-card>mat-card>h3[data-test-id='location-card-country']")
                if(len(countryElements)>0):
                    partner.locations=[c.text for c in countryElements]
                locationCards=locationListContainer.find_elements(By.CSS_SELECTOR,"app-location-card")
                if(len(locationCards)>0):
                    mainLocCard=locationCards[0]
                    addr=mainLocCard.find_elements(By.CSS_SELECTOR,"a[data-test-id='location-card-address']")
                    if(len(addr)>0):
                        partner.contactDetails.address=addr[0].text

            except:
                print("No location section in partner ",ind+1)

            # writeNewData(partners=[partner],sheet="Google")
            print(partner.name,"\n")
            driver.back()
        lastVisitedIndex=ind
        print("Clicking button after ",ind+1," partners")
        try:
            moreButton=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.load-more-container>button")))
            moreButton.click()
        except:
            print("\n-------------------------\nCannot load more after ",lastVisitedIndex," partners\n-----------------------------\n")
            break
    driver.quit()

getPartnerList()