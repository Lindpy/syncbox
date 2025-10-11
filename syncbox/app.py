import os
import threading
import time
import webbrowser
from typing import List

import uvicorn
from deezerapi import selected_to_deezer
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from xmlprocessing import parse_xml_data

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

folder = r"C:\Users\lilia\src\syncbox\tests\testxmls"
library = parse_xml_data()
tree = library.playlist


app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def read_tree(request: Request):
    return templates.TemplateResponse("tree.html", {"request": request, "tree": tree})


@app.post("/", response_class=HTMLResponse)
def get_selected(request: Request, selected: List[str] = Form(...)):
    selected_to_deezer(library, selected)
    return templates.TemplateResponse(
        "selected.html", {"request": request, "selected": selected}
    )


def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8000")


def syncbox_():
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)


syncbox_()
