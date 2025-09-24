# import numpy as np
# import joblib
# import warnings
# from fastapi import FastAPI, Request, Form
# from fastapi.templating import Jinja2Templates
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# warnings.filterwarnings('ignore')

# model = joblib.load("model_Fraud.joblib")
# enc = joblib.load("encoder_Fraud.joblib")


# #data[0] = int(enc.transform([data[0]]))

# #print(model.predict([data]))
# def prediction(type_: str, amount: float, oldBal1: float, newBal1: float,
#                oldBal2: float, newBal2: float):
#     data = [type_.upper(), amount, oldBal1, newBal1, oldBal2, newBal2]
#     data[0] = int(enc.transform([data[0]]))
#     return int(model.predict([data]))

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # change to your frontend domain in prod
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# #templates = Jinja2Templates(directory="templates")

# #app.mount("/static", StaticFiles(directory="static"), name="static")

# # @app.get("/",response_class=HTMLResponse)
# # async def read_form(request: Request):
# #     return templates.TemplateResponse("form.html", {"request":request})

# @app.post("/predict")
# async def get_prediction(request: Request,type_:str = Form(...),amount:float = Form(...),oldBal1:float = Form(...),newBal1:float = Form(...),oldBal2:float = Form(...),newBal2:float = Form(...)):
#     result = prediction(type_,amount,oldBal1,newBal1,oldBal1,newBal2)
#     message = "Fraud Detected!" if result == 1 else "No Fraud Detected."
#     return {"result": message}
    

import joblib
import warnings
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

warnings.filterwarnings("ignore")

model = joblib.load("model_Fraud.joblib")
enc = joblib.load("encoder_Fraud.joblib")

def prediction(type_: str, amount: float, oldBal1: float, newBal1: float,
               oldBal2: float, newBal2: float):
    data = [type_.upper(), amount, oldBal1, newBal1, oldBal2, newBal2]
    data[0] = int(enc.transform([data[0]]))
    return int(model.predict([data]))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod, restrict to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1) Mount built frontend files
#app.mount("/static", StaticFiles(directory="dist/assets"), name="static")

# 2) Serve index.html at root

# API route
@app.post("/predict")
async def get_prediction(
    type_: str = Form(...),
    amount: float = Form(...),
    oldBal1: float = Form(...),
    newBal1: float = Form(...),
    oldBal2: float = Form(...),
    newBal2: float = Form(...),
):
    result = prediction(type_, amount, oldBal1, newBal1, oldBal2, newBal2)
    message = "Fraud Detected!" if result == 1 else "No Fraud Detected."
    return {"result": message}


app.mount("/", StaticFiles(directory="dist", html=True), name="frontend")