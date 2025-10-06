from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os 

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # folder where HTML lives


from typing import List
from pydantic import BaseModel

class Branch(BaseModel):
    name: str
    data: str
    leaves: List['Branch'] = []


tree = Branch(
    name="Root",
    data="root_data",
    leaves=[
        Branch(name="Folder1", data="data1", leaves=[]),
        Branch(
            name="Folder2",
            data="data2",
            leaves=[
                Branch(name="Subfolder1", data="data3", leaves=[]),
                Branch(name="Subfolder2", data="data4", leaves=[]),
            ],
        ),
    ],
)



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@app.get("/", response_class=HTMLResponse)
def read_tree(request: Request):
    return templates.TemplateResponse("tree.html", {"request": request, "tree": tree})

@app.post("/", response_class=HTMLResponse)
def get_selected(request: Request, selected: List[str] = Form(...)):
    return templates.TemplateResponse("selected.html", {"request": request, "selected": selected})

