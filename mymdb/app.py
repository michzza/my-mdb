from fastapi import FastAPI
import sqlite3



app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello" : "World"}


@app.get("/titles/{title_id}")
def read_item(title_id):
    con = sqlite3.connect('mymdb.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()


    cur.execute("""SELECT * FROM titles WHERE id = ?;""", [title_id])
    result = cur.fetchone()
    con.close()
    return result