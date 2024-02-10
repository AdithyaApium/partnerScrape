import json


class PartnerContact:
    phone:str
    email:str
    address:str
    web:str

    def __str__(self) -> str:
        return str(self.__dict__)
    
class Partner:
    def __init__(self) -> None:
        self.contactDetails=PartnerContact()
    name:str
    specializations:list[str]
    locations:list[str]
    source:str
    partnerPage:str
    contactDetails:PartnerContact

    def __str__(self) -> str:
        return str(self.__dict__)

