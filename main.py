from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
app=FastAPI()

class Patient(BaseModel):
   
   id:Annotated[str,Field(...,description="id of patient")]
   name:Annotated[str,Field(...,description="name of the patient")]
   city:Annotated[str,Field(...,description="city where patient is living")]
   age:Annotated[int,Field(...,gt=0,le=120,description="city of th e patient")]
   gender: Annotated[
           Literal["male", "female", "others"],
           Field(..., description="Gender of the patient")
       ]
   height:Annotated[float,Field(...,gt=0,description='Heigth of the patient')]
   weight:Annotated[float,Field(...,description="weight of the patient")]

   @computed_field
   @property
   def bmi(self)->float:
      bmi=round(self.weight/(self.height**2),2)
      return bmi

   @computed_field
   @property
   def verdict(self)->float:
      if self.bmi<18.5:
         return "underweight"
      elif self.bmi<25:
         return"Normal"
      elif self.bmi<30:
         return "Normal"
      else:
         return "Obese"
      


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]






#helper function to load json file
def load_data():
    with open('patients.json','r') as f:
     data=json.load(f)
     return data

def save_data(data):
   with open("patients.json",'w') as f:
      json.dump(data,f)

@app.get("/")
def hello():
    return {"message":"Patient management system API"} 

@app.get('/about')
def about():
    return {"message":'fully functional api to manage patient records'}

@app.get('/view')
def view():
   data=load_data()

   return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description="Id of pa tient in db",example="P001")):
   data=load_data()

   if patient_id in data:
      return data[patient_id]
   raise HTTPException(status_code=400,detail="Patient not found")


@app.get('/sort')
def sort_patients(
    sort_by: str = Query(
        ...,
        description='Sort on the basis of height, weight or bmi',
    ),
    order: str = Query('asc', description='sort in asc or desc order'),
):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f'Invalid field select from {valid_fields}',
        )
    if order not in ['asc','desc']:
       raise HTTPException(status_code=400,detail="invalid order")
    data=load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order )

    return sorted_data

#post endpoint

@app.post("/create")
def create_patient(patient:Patient):

   data=load_data()

   if patient.id in data:
      raise HTTPException(400,detail="Patient already exists")

   data[patient.id]=patient.model_dump(exclude=["id"])

   #save data
   save_data(data)

   return JSONResponse(status_code=201,content={"message":"patient created successfully"})

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:PatientUpdate):
   data=load_data()

   if patient_id not in data:
      raise HTTPException(status_code=404,detail="Patient not found")

   existing_patient_info=data[patient_id]

   updated_patient_info=patient_update.model_dump(exclude_none=True)

   for key,value in updated_patient_info.items():

      existing_patient_info[key]=value

   #existing patient info ->pydantic obejct->update bmi->verdit
   existing_patient_info['id']=patient_id
   patient_pydantic_obj=Patient(**existing_patient_info)

   existing_patient_info=patient_pydantic_obj.model_dump(exclude='id')
   #add dictionary to data

   data[patient_id]=existing_patient_info

   #save
   save_data(data)

   return JSONResponse(status_code=200,content="Patient details updated succesfully")