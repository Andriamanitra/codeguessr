import sqlite3
import urllib.parse
from sanic import Sanic
from sanic.response import json
from sanic import exceptions

app = Sanic("CodeGuessr")

# allow connecting from vite ("npm run dev")
# app.extend(config={"cors_origins": "http://localhost:5173"})

DB_URI = "file:rosettacodes.db?mode=ro"

def codes_from_db(db_uri: str, num_solutions: int = 15) -> list[dict]:
    result = []
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute(
            "SELECT id, task_name, lang, code"
            " FROM solutions"
            " ORDER BY random()"
            " LIMIT ?", (num_solutions,))
        for solution_id, task_name, lang, code in res.fetchall():
            escaped_task_name = urllib.parse.quote(task_name)
            result.append({
                "solution_id": solution_id,
                "task_name": task_name,
                "task_url": f"https://rosettacode.org/wiki/{escaped_task_name}",
                "language": lang,
                "code": code,
            })
    return result

def langs_from_db(db_uri: str) -> list[str]:
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute("SELECT DISTINCT(lang) FROM solutions")
        return [lang for (lang,) in res.fetchall()]


def solution_from_db(db_uri: str, solution_id) -> dict:
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute(
            "SELECT task_name, lang, code"
            " FROM solutions"
            " WHERE id = ?", (solution_id,))
        found = res.fetchone()

    if found is None:
        raise exceptions.NotFound(f"Could not find a solution with id={solution_id}")

    task_name, lang, code = found
    escaped_task_name = urllib.parse.quote(task_name)
    return {
        "solution_id": solution_id,
        "task_name": task_name,
        "task_url": f"https://rosettacode.org/wiki/{escaped_task_name}",
        "language": lang,
        "code": code
    }

@app.get("/api/solution/<solution_id:int>")
async def api_solution(req, solution_id: int):
    return json(solution_from_db(DB_URI, solution_id))

@app.get("/api/randoms")
async def api_randoms(req):
    return json(codes_from_db(DB_URI))

@app.get("/api/langs")
async def api_langs(req):
    return json(langs_from_db(DB_URI))


app.static("/assets", "./frontend/dist/assets/")
app.static("/", "./frontend/dist/index.html", name="index")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False, access_log=False)
