from fastapi import FastAPI,Path,HTTPException,Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
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