from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from classes.partnerData import Partner, PartnerContact

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

gPartnerLink="https://cloud.google.com/find-a-partner/"

def getPartnerList()->list[Partner]:
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
        if((not cardCount>currentCardCount) or cardCount>1):
            break
        currentCardCount=cardCount
        print("Found cards",cardCount," - ",currentCardCount)
        try:
            moreButton=wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"div.load-more-container>button")))
            moreButton.click()
        except:
            break

    finalCardList=driver.find_elements(By.CSS_SELECTOR,"a[data-test-id='partner-link']")
    for i,card in enumerate(finalCardList):
        partnerNameElement=card.find_elements(By.CSS_SELECTOR,"h2[data-test-id='partner-name']")

        partnerName=specList=locations=partnerGCPage="N/A"

        partnerGCPage=card.get_attribute("href")
        
        if(len(partnerNameElement)>0):
            partnerName=partnerNameElement[0].text
        specListELement=card.find_elements(By.CSS_SELECTOR,"div[data-test-id='specializations-data']")
        if(len(specListELement)>0):
            specList=specListELement[0].text
        locationsElement=card.find_elements(By.CSS_SELECTOR,"mat-icon")
        if(len(locationsElement)>0):
            imgText=locationsElement[0].text
            if(imgText=="place"):
                locations=locationsElement[0].find_element(By.XPATH, "following-sibling::*[1]").text
        # Create a partner obj and set values
        p = Partner()
        p.source="Google"
        p.name=partnerName
        p.specializations=specList.split(",")
        p.locations=locations.split(",")
        p.partnerPage=partnerGCPage

        # partnerObj={"name":partnerName,"specializations":specList,"locations":locations,"gcPage":partnerGCPage}
        finalPartnerObjList.append(p)

    # Get contact details per each
    for pInd,partner in enumerate(finalPartnerObjList):
        website=phone=mapUrl=email="N/A"
        driver.get(partner.partnerPage)
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"app-contact-icons>h2")))
        
            contactDetails=driver.find_elements(By.CSS_SELECTOR,"h2[title='Contact Details']")
            if(len(contactDetails)>0):
                websiteElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner website']")
                if(len(websiteElement)>0):
                    website=websiteElement[0].get_attribute("href")
                emailElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner email address']")
                if(len(emailElement)>0):
                    email=emailElement[0].get_attribute("href").split("mailto:")[1]
                phoneElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner phone number']")
                if(len(phoneElement)>0):
                    phone=phoneElement[0].get_attribute("href").split("tel:")[1]
                mapElement=driver.find_elements(By.CSS_SELECTOR,"a[aria-label='Partner address']")
                if(len(mapElement)>0):
                    mapUrl=mapElement[0].get_attribute("href")

                pContact=PartnerContact()
                pContact.address=mapUrl
                pContact.email=email
                pContact.phone=phone
                pContact.web=website
                finalPartnerObjList[pInd].contactDetails=pContact
                # print({"website":website,"email":email,"phone":phone,"address":mapUrl})
                break
        except:
                    print("No contact")
                    continue
    driver.quit()
    return finalPartnerObjList

# getPartnerList()