import json


class PartnerContact:
    def __init__(self) -> None:
        self.phone=self.email=self.address=self.web="N/A"
    phone:str
    email:str
    address:str
    web:str

    
class Partner:
    def __init__(self) -> None:
        self.contactDetails=PartnerContact()
        self.name=self.source=self.partnerPage="N/A"
        self.specializations=self.locations=["N/A"]
    name:str
    specializations:list[str]
    locations:list[str]
    source:str
    partnerPage:str
    contactDetails:PartnerContact


