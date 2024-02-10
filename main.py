from selenium import webdriver

# Import scrapers
from scrapers.gPartners import getPartnerList as getGooglePartners

def main():
    gpartnersList=getGooglePartners()


if __name__=="__main__":
    main()