from pydantic import BaseModel



class Address(BaseModel):

    city:str
    state:str
    pin:str 

class Patient(BaseModel):
    name:str
    gender:str
    age:int
    address:Address

address_dict={"city":"rawalpindi","state":"Punjab","pin":"52000"}



address1=Address(**address_dict)
patient_dict={"name":"abdul","gender":"male","age":20,"address":address1}

patient1=Patient(**patient_dict)
print(patient1)
print(patient1.address.city)