# CodeGuessr

If you thought https://guessthiscode.com/ is fun but just *too easy* you have come to the right place.
We leverage a large set of example programs on [Rosetta Code](https://rosettacode.org/wiki/Rosetta_Code) to
create a much more challenging (thousands of programs, hundreds of different languages!) programming language guessing game.

## Instructions to run locally

1. Download an XML file containing all the "Programming Task" category pages from Rosetta Code: https://rosettacode.org/wiki/Special:Export
1. Create a virtual environment to install Python dependencies in (for example `python3 -m virtualenv venv`)
1. `pip install lxml` which is used to parse the XML file
1. `python3 parse_to_db.py ROSETTA_EXPORT.xml` to parse the solutions into a sqlite3 database `rosettacodes.db`
1. (Optional) `sqlite3 rosettacodes.db -init cleanup.sql` to clean up the database (removes the most niche languages and extremely short solutions, fixes some inconsistent naming, etc.)
1. `pip install sanic[ext]` which is used to serve the API and static files
1. `sanic -d server.app` to run the server (in development mode)
1. `VITE_API_URL="http://localhost:8000" cd frontend && npm run dev` to run the frontend locally (you may need to uncomment
the line that allows cross-origin requests from localhosts in `server.py`)
