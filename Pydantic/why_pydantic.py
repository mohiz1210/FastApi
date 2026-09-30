from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Literal,Optional

class Patient(BaseModel):
    name:str
    email:EmailStr
    linkedin_url:AnyUrl
    age:int
    weight:float=Field(gt=0)
    married:bool=False
    allergies:Optional[List[str]]=None
    contact_details:Dict[str,str]


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('inserted')

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('updated')

patient_info={'name':'abdul','email':'abc@gmail.com',"linkedin_url":"http://linked.com/123",'age':20,"weight":7.2,"married":True,"contact_details":{"phone":"123456789"}}

patient1=Patient(**patient_info)

insert_patient_data(patient1)
update_patient_data(patient1)