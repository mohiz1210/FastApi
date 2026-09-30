from pydantic import BaseModel, EmailStr, Field,computed_field
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    height:float
    married: bool
    allergies: Annotated[Optional[List[str]], Field(default=None)]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def calculate_bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi

 


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('BMI',patient.calculate_bmi)
    print('updated')


patient_info = {
    'name': 'abdul',
    'email': 'abc@gmail.com',
    'age': 70,
    'weight': 70.2,
    'height':5.4,
    'married': True,
    'contact_details': {
        'phone': '123456789',
        'emergency':"324555"
    }
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)