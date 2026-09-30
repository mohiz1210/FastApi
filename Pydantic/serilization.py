from pydantic import BaseModel



class Address(BaseModel):

    city:str
    state:str
    pin:str 

class Patient(BaseModel):
    name:str
    gender:str="Male"
    age:int
    address:Address

address_dict={"city":"rawalpindi","state":"Punjab","pin":"52000"}



address1=Address(**address_dict)
patient_dict={"name":"abdul","age":20,"address":address1}

patient1=Patient(**patient_dict)
#temp=patient1.model_dump(exclude={'address':['state']})
temp=patient1.model_dump(exclude_unset=True)
temp1=patient1.model_dump_json()
print(temp)
print(temp1)