import sqlite3
from typing import TypedDict
import urllib.parse
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.response import json
from sanic.exceptions import NotFound
from sanic_ext import openapi

app = Sanic("CodeGuessr")

# allow connecting from vite ("npm run dev")
# app.extend(config={"cors_origins": "http://localhost:5173"})

DB_URI = "file:rosettacodes.db?mode=ro"


class Solution(TypedDict):
    solution_id: int
    task_name: str
    task_url: str
    language: str
    code: str


class ErrorJSON(TypedDict):
    description: str
    status: int
    message: str


def codes_from_db(db_uri: str, num_solutions: int = 15) -> list[Solution]:
    result = []
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute(
            "SELECT id, task_name, lang, code"
            " FROM solutions"
            " ORDER BY random()"
            " LIMIT ?", (num_solutions,))
        for solution_id, task_name, lang, code in res.fetchall():
            escaped_task_name = urllib.parse.quote(task_name)
            solution = Solution(
                solution_id=solution_id,
                task_name=task_name,
                task_url=f"https://rosettacode.org/wiki/{escaped_task_name}",
                language=lang,
                code=code
            )
            result.append(solution)
    return result


def langs_from_db(db_uri: str) -> list[str]:
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute("SELECT DISTINCT(lang) FROM solutions")
        return [lang for (lang,) in res.fetchall()]


def solution_from_db(db_uri: str, solution_id: int) -> Solution:
    with sqlite3.connect(db_uri, uri=True) as conn:
        res = conn.execute(
            "SELECT task_name, lang, code"
            " FROM solutions"
            " WHERE id = ?", (solution_id,))
        found = res.fetchone()

    if found is None:
        raise NotFound(f"Could not find a solution with id={solution_id}")

    task_name, lang, code = found
    escaped_task_name = urllib.parse.quote(task_name)
    return Solution(
        solution_id=solution_id,
        task_name=task_name,
        task_url=f"https://rosettacode.org/wiki/{escaped_task_name}",
        language=lang,
        code=code
    )


@app.get("/api/solution/<solution_id:int>")
@openapi.response(200, {"application/json": Solution}, "OK")
@openapi.response(404, {"application/json": ErrorJSON}, "Not found")
async def api_solution(req: Request, solution_id: int) -> HTTPResponse:
    """Get a solution by id"""
    return json(solution_from_db(DB_URI, solution_id))


@app.get("/api/randoms")
@openapi.response(200, {"application/json": list[Solution]}, "OK")
async def api_randoms(req: Request) -> HTTPResponse:
    """Get a list of random solutions"""
    return json(codes_from_db(DB_URI))


@app.get("/api/langs")
@openapi.response(200, {"application/json": list[str]}, "OK")
async def api_langs(req: Request) -> HTTPResponse:
    """Get a list of available programming languages"""
    return json(langs_from_db(DB_URI))


app.static("/", "./frontend/dist/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=False, access_log=False)
