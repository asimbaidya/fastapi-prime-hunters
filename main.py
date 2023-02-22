from datetime import datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.prime import is_prime
import sqlite3


# init fastapi
app = FastAPI()

# init jinja2
templates = Jinja2Templates(directory="templates")

# connecting db
con: sqlite3.Connection = sqlite3.connect("primes.db")
cur: sqlite3.Cursor = con.cursor()
# create table
cur.execute("CREATE TABLE IF NOT EXISTS primes(prime INTEGER, time varchar(30))")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):

    res = cur.execute("SELECT * FROM primes order by prime asc")
    primes = res.fetchall()

    return templates.TemplateResponse(
        "index.html", {"request": request, "primes": primes}
    )


@app.post("/verify")
async def check(request: Request, prime: int = Form(...)):

    primes = []
    msg: str = ""
    msg_class: str = ""

    if prime < 0 or prime > 42_000_000_0000_000:
        msg: str = "Prime must be in this range (1,42_000_000_0000_000)"
    elif not is_prime(prime):
        msg: str = f"Ops, {prime} is not a prime"
        msg_class: str = "warn"
    else:

        # fetchign all primes from db
        res = cur.execute("SELECT * FROM primes")
        primes = res.fetchall()

        # check if prime already exists
        ok = True
        for p in primes:
            if p[0] == prime:
                ok = False
                msg = f"{p[0]} already discovered [{p[1]}]"
                msg_class = "warn"
                break
        if ok:
            # all good so insert now insert
            time_posted = datetime.now().strftime("%d/%m/%Y|%H:%M:%S")
            sql = f'INSERT INTO primes VALUES ({prime},"{time_posted}")'
            cur.execute(sql)
            con.commit()
            msg = f"congratulation, for the very firt time {prime} is verified as a prime!"
            msg_class = "success!"

    # fetchign again with updated prime
    res = cur.execute("SELECT * FROM primes order by prime asc")
    primes = res.fetchall()

    return templates.TemplateResponse(
        "verify.html",
        {"request": request, "primes": primes, "msg": msg, "msg_class": msg_class},
    )
