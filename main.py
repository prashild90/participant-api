fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="Participant Records API")

class Participant(BaseModel):
    name: str
    age: int
    site: str

@app.on_event("startup")
def startup():
    conn = sqlite3.connect("participants.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS participants
                    (id INTEGER PRIMARY KEY, name TEXT, age INTEGER, site TEXT)""")
    conn.commit()
    conn.close()

@app.get("/participants")
def get_all():
    conn = sqlite3.connect("participants.db")
    rows = conn.execute("SELECT * FROM participants").fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "age": r[2], "site": r[3]} for r in rows]

@app.post("/participants")
def create(p: Participant):
    conn = sqlite3.connect("participants.db")
    conn.execute("INSERT INTO participants (name, age, site) VALUES (?,?,?)",
                 (p.name, p.age, p.site))
    conn.commit()
    conn.close()
    return {"status": "created"}

@app.delete("/participants/{id}")
def delete(id: int):
    conn = sqlite3.connect("participants.db")
    conn.execute("DELETE FROM participants WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

