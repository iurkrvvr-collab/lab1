from fastapi import FastAPI, Request, Form  
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models import Cat
from db import load_database  
    
DATABASE = load_database()
        
app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    cats = DATABASE.get_all()
    cats_count = len(cats)
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "cats_count": cats_count,
            "cats": cats
        }
    )

@app.get("/info", response_class=HTMLResponse)
def info(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, 
        name="info.html", 
        context={"title": "Інформація"}
    )

@app.get("/cats/new", response_class=HTMLResponse)
def new_cat_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="new_cat.html", context={})

@app.post("/cats/new", response_class=HTMLResponse)
def create_cat(
    request: Request, 
    id: int = Form(...), 
    name: str = Form(...), 
    photo: str = Form(...), 
    age: int = Form(...)
) -> HTMLResponse:
    new_cat = Cat(id=id, name=name, photo=photo, age=age)
    DATABASE.add_cat(new_cat)  
    
    cats = DATABASE.get_all()
    return templates.TemplateResponse(
        request=request, name="index.html", context={"cats_count": len(cats), "cats": cats}
    )

@app.get("/{id}", response_class=HTMLResponse)
def cat(request: Request, id: int) -> HTMLResponse:
    cat = DATABASE.get_by_id(id)
    return templates.TemplateResponse(
        request=request, name="cat.html", context={
            "cat_id": id,
            "cat": cat
        }
    )