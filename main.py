from selenium import webdriver
from GSheets.updateSheet import writeNewData

# Import scrapers
from scrapers.gPartners import getPartnerList as getGooglePartners

def main():
    gpartnersList=getGooglePartners()
    writeNewData(gpartnersList)


if __name__=="__main__":
    main()