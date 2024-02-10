from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from GSheets.updateSheet import writeNewData

from classes.partnerData import Partner, PartnerContact
from utils.stringUtils import stringArrayToStr

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

gPartnerLink="https://cloud.google.com/find-a-partner/"

global lastVisitedIndex
lastVisitedIndex=-1

def getPartnerList():
    global lastVisitedIndex
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(gPartnerLink)
    wait=WebDriverWait(driver=driver,timeout=5)
    currentCardCount=0

    finalPartnerObjList:list[Partner]=[]
    
    while True:
        wait.until(lambda driver:(len(driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']")))>currentCardCount)
        cardCount=len(driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']"))
        print("Card count updated from ",currentCardCount," to ",cardCount)
        # Temporarily limited to 12 elements
        if((not cardCount>currentCardCount)):
            break
        currentCardCount=cardCount
        print("Found cards",cardCount," - ",currentCardCount)

        
        for ind in range(lastVisitedIndex+1,cardCount):
            loadedCards=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"a[data-test-id='partner-link']")))
            print("Starting from partner ",ind+1)
            try:
                partner=Partner()
                partner.source="Google"
                loadedCards[ind].click()
            except:
                print("Error clicking card ",ind+1)
            try:
                wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"app-contact-icons>h2")))
            
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
                nameElement=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"h1[data-test-id='title']")))
                partner.name=nameElement.text
            except:
                print("No name in partner ",ind+1)

            try:
                specContainer=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"p[data-test-id='specializations-data']")))
                partner.specializations=specContainer.text.split(",")
            except:
                print("No specs in partner ",ind+1)

            try:
                locationListContainer=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.detail-locations")))
                countryElements=locationListContainer.find_elements(By.CSS_SELECTOR,"app-location-card>mat-card>h3[data-test-id='location-card-country']")
                if(len(countryElements)>0):
                    countries=stringArrayToStr([t.text for t in countryElements])
                    partner.locations=countries
                locationCards=locationListContainer.find_elements(By.CSS_SELECTOR,"app-location-card")
                if(len(locationCards)>0):
                    mainLocCard=locationCards[0]
                    addr=mainLocCard.find_elements(By.CSS_SELECTOR,"a[data-test-id='location-card-address']")
                    if(len(addr)>0):
                        partner.contactDetails.address=addr[0].text

            except:
                print("No location section in partner ",ind+1)

            writeNewData(partners=[partner])
            driver.back()
        lastVisitedIndex=ind
        print("Clicking button after ",ind+1," partners")
        try:
            moreButton=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.load-more-container>button")))
            moreButton.click()
        except:
            print("\n-------------------------\nCannot load more after ",lastVisitedIndex," partners\n-----------------------------\n")
            break

    # finalCardList=driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']")
    # for i,card in enumerate(finalCardList):
    #     partnerNameElement=card.find_elements(By.CSS_SELECTOR,"h2[data-test-id='partner-name']")

    #     partnerName=specList=locations=partnerGCPage="N/A"

    #     partnerGCPage=card.get_attribute("href")
        
    #     if(len(partnerNameElement)>0):
    #         partnerName=partnerNameElement[0].text
    #     specListELement=card.find_elements(By.CSS_SELECTOR,"div[data-test-id='specializations-data']")
    #     if(len(specListELement)>0):
    #         specList=specListELement[0].text
    #     locationsElement=card.find_elements(By.CSS_SELECTOR,"mat-icon")
    #     if(len(locationsElement)>0):
    #         imgText=locationsElement[0].text
    #         if(imgText=="place"):
    #             locations=locationsElement[0].find_element(By.XPATH, "following-sibling::*[1]").text
    #     # Create a partner obj and set values
    #     p = Partner()
    #     p.source="Google"
    #     p.name=partnerName
    #     p.specializations=specList.split(",")
    #     p.locations=locations.split(",")
    #     p.partnerPage=partnerGCPage

    #     # partnerObj={"name":partnerName,"specializations":specList,"locations":locations,"gcPage":partnerGCPage}
    #     finalPartnerObjList.append(p)

    # # Get contact details per each
    # for pInd,partner in enumerate(finalPartnerObjList):
    #     website=phone=mapUrl=email="N/A"
    #     driver.get(partner.partnerPage)
    #     try:
    #         wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"app-contact-icons>h2")))
        
    #         contactDetails=driver.find_elements(By.CSS_SELECTOR,"h2[title='Contact Details']")
    #         if(len(contactDetails)>0):
    #             websiteElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner website']")
    #             if(len(websiteElement)>0):
    #                 website=websiteElement[0].get_attribute("href")
    #             emailElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner email address']")
    #             if(len(emailElement)>0):
    #                 email=emailElement[0].get_attribute("href").split("mailto:")[1]
    #             phoneElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner phone number']")
    #             if(len(phoneElement)>0):
    #                 phone=phoneElement[0].get_attribute("href").split("tel:")[1]
    #             mapElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner address']")
    #             if(len(mapElement)>0):
    #                 mapUrl=mapElement[0].get_attribute("href")

    #             pContact=PartnerContact()
    #             pContact.address=mapUrl
    #             pContact.email=email
    #             pContact.phone=phone
    #             pContact.web=website
    #             finalPartnerObjList[pInd].contactDetails=pContact
    #             # print({"website":website,"email":email,"phone":phone,"address":mapUrl})
    #             break
    #     except:
    #                 print("No contact")
    #                 continue
    driver.quit()

getPartnerList()