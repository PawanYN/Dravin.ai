REM--------------1. create/activate env -----
IF NOT EXIST ".venv" (py -3 -m venv .venv)

CALL .venv\Scripts\activate.bat

pip install -r requirements.txt

REM ------------2. load env vars from .env-------
FOR /F "usebackq tokens=*" %%A IN (`type backend\.env ^| findstr /V "^#"`) DO set %%A

REM -------- 3. run migrations if alembic present --------
IF EXIST backend\alembic (
    alembic -c backend\alembic.ini upgrade head
)

REM -------- 4. start API --------
uvicorn app.main:app --reload