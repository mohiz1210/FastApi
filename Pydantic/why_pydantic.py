from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Literal,Optional,Annotated

class Patient(BaseModel):
    name:Annotated[str,Field(max_length=50,title="Name of Patient",description="give the name of the patient in less than 50 words ",examples=["abdul","mohiz"])]
    email:EmailStr
    linkedin_url:AnyUrl
    age:int=Field(gt=0,lt=120)
    weight:Annotated[float,Field(gt=0,strict=True)]
    married:Annotated[bool,Field(default=None,description="is the patient married or not")]
    allergies:Annotated[Optional[List[str]],Field(default=None)]
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