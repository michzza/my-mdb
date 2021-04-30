from fastapi import FastAPI, Request
import sqlite3
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



app = FastAPI()

templates = Jinja2Templates(directory="mymdb/templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, search: str = ""):
    results = []  
    if search != "":
        con = sqlite3.connect('mymdb.db')
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("""SELECT * FROM titles 
            WHERE primary_title LIKE ? 
            AND type = 'movie'
            LIMIT 15;""", ['%' + search + '%'])
        results = cur.fetchall()
        con.close()
    return templates.TemplateResponse("home.html", {'request': request, 'search' : search, 'results' : results})

@app.get("/titles/{title_id}", response_class=HTMLResponse)
def read_item(request: Request, title_id):
    con = sqlite3.connect('mymdb.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute("""SELECT * FROM titles WHERE id = ?;""", [title_id])
    result = cur.fetchone()
    con.close()
    return templates.TemplateResponse("film.html", {'request': request, 'result' : result})
