import numpy as np
import joblib
import warnings
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
warnings.filterwarnings('ignore')

model = joblib.load("model_Fraud.joblib")
enc = joblib.load("encoder_Fraud.joblib")

data = ["CASH_OUT",181.00,181.0,0,21182.0,0]
#data[0] = int(enc.transform([data[0]]))

#print(model.predict([data]))
def prediction(type_:str,amount:float,oldBal1:float,newBal1:float,oldBal2:float,newBal2:float):
    data = [type_.upper(),amount,oldBal1,newBal1,oldBal1,newBal2]
    data[0] = int(enc.transform([data[0]]))
    return int(model.predict([data]))

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request":request})

@app.post("/predict",response_class=HTMLResponse)
async def get_prediction(request: Request,type_:str = Form(...),amount:float = Form(...),oldBal1:float = Form(...),newBal1:float = Form(...),oldBal2:float = Form(...),newBal2:float = Form(...)):
    result = prediction(type_,amount,oldBal1,newBal1,oldBal1,newBal2)
    message = "Fraud Detected!" if result == 1 else "No Fraud Detected."
    return templates.TemplateResponse("result.html", {'request': request,'result':message})
    
