from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from GSheets.updateSheet import writeNewData

from classes.partnerData import Partner
from utils.stringUtils import stringArrayToStr

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

ciscoPartnersLink="https://locatr.cloudapps.cisco.com/WWChannels/LOCATR/pf/index.jsp#/"

def getPartnerList():
    driver=webdriver.Chrome(options=chrome_options)
    driver.get(ciscoPartnersLink)
    wait=WebDriverWait(driver=driver,timeout=10)
    finalPartnerList:List[Partner]=[]

    currentIndex=0
    currentPage=0
    while True:
        while True:
            cardList=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div.__MR_HOME_SEARCH_MAIN_RESULTS__>ul>li")))
            if(len(cardList)<=currentIndex):break
            try:
                card=cardList[currentIndex]
                partner=Partner()
                partner.source="Cisco"
                card.click()

                headers=wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,"section>h4")))
                specHeader=[h for h in headers if h.text.find("Specializations")>-1]
                if(len(specHeader)>0):
                    specList=specHeader[0].find_element(By.XPATH,"..").find_elements(By.CSS_SELECTOR,"ul>li")
                    partner.specializations=[spec.text for spec in specList]

                contactDetailSection=wait.until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,"body>div>div>div>div>div>section>h3")))
                if(len(contactDetailSection)>0):
                    partner.name=contactDetailSection[0].text
                    addrSectionList=contactDetailSection[0].find_element(By.XPATH,"..").find_elements(By.CSS_SELECTOR,"div.text-cc-body-medium>p")
                    if(len(addrSectionList)>0):
                        address=stringArrayToStr([a.text for a in addrSectionList])
                        partner.contactDetails.address=address
                        partner.locations=[addrSectionList[-1].text]

                    phoneSection=contactDetailSection[0].find_element(By.XPATH,"..").find_elements(By.CSS_SELECTOR,"div>p>a")
                    if(len(phoneSection)>0):
                        pList=[p for p in phoneSection if p.get_attribute("href").find("tel")>-1]
                        if(len(pList)>0):
                            phone=pList[0].text
                            partner.contactDetails.phone=phone
                        webList=[p for p in phoneSection if p.get_attribute("href").find("tel")<0]
                        if(len(webList)>0):
                            web=webList[0].text
                            partner.contactDetails.web=web
                # Add each partner to sheet
                writeNewData(partners=[partner])
                driver.back()
                currentIndex+=1
            except:
                print("Error at page ",currentPage+1," partner ",currentIndex+1)
                driver.back()
                currentIndex+=1
                continue
        try:
            btnList=wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"nav>ul>li>a.group>span")))
            nextBtn=[b for b in btnList if b.text=="Next"]
            if(len(nextBtn)>0):
                nextBtn[0].find_element(By.XPATH,"..").find_element(By.XPATH,"..").click()
                currentIndex=0
                currentPage+=1
            else:break
        except:
            print("Error clicking next btn at page ",currentPage+1)
            break
        


    driver.quit()

getPartnerList()