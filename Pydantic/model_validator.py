from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import List, Dict, Optional, Annotated


class Patient(BaseModel):
    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Annotated[Optional[List[str]], Field(default=None)]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    def validate_emergency_contacts(cls,model):

        if model.age > 60 and 'emergency' not in model.contact_details:
            raise ValueError(
                "Patient older than 60 must have an emergency contact"
            )

        return model


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print('updated')


patient_info = {
    'name': 'abdul',
    'email': 'abc@hdfc.com',
    'age': 70,
    'weight': 7.2,
    'married': True,
    'contact_details': {
        'phone': '123456789',
        'emergency':"324555"
    }
}

patient1 = Patient(**patient_info)

update_patient_data(patient1)