from fastapi import FastAPI, Request
from pydantic import BaseModel
from transactionhist import *
import pickle
import time
from masterDB import *
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

pkl_file = open('cats_new.pkl', 'rb')
cats_dict = pickle.load(pkl_file)
pkl_file.close()

# to run the app vvv
# uvicorn main:app --reload


# Instansiate FastAPI Class
# when running the model, "main" is the python file and "app"
# is the variable name that is holding the FastAPI class (main:app)
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def root():
    # Written as a dict but returns a json object
    return {"message": 'Hello World!'}

@app.post("/transaction/")
def transaction(full_dict: dict):
    start_time = time.time()
    trans = TransactionHistory(full_dict=full_dict)
    request = trans.getCats(cats_dict=masterPull())
    print("--- %s seconds ---" % (time.time() - start_time))
    return request

@app.get("/create_master/")
def create_master():
    createMaster()
    return{"message": "Master DB has been created"}

@app.get("/admin")
async def testing(request: Request,
                  Cat: str = 'None',
                  Plaid_cat: str = 'None',
                  Destination: str = 'None'):

    # If Value and Destination have values, update the database
    if (Plaid_cat != 'None') & (Destination != 'None'):
        
        return {"Cat": Cat,"Plaid Cat": Plaid_cat, "message": Destination}

    Dict = masterPull()
    cats = list(Dict.keys())

    return templates.TemplateResponse("admin.html",
                                     {'request': request,
                                      'cats': cats,
                                      'Cat': Cat,
                                      'Dict': Dict,
                                      'Plaid_cat': Plaid_cat,
                                      'Destination': Destination})


@app.get("/test")
def testing(Value: str):
    new_val = Value
    return {"message": new_val}
