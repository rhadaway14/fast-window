start for windows:
uvicorn app.main:app --reload 

start for ubuntu:
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 --bind 0.0.0.0:8000

///////////////////////////////////////////////////////////////////////////////////////////////

apache benchmark load_test:
ab -n 100 -c 10 http://localhost:8000/api/v1/transaction/loadtest/txn123

///////////////////////////////////////////////////////////////////////////////////////////////

CRUD examples:

POST:

curl -X POST http://localhost:8000/api/v1/transaction/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "loadtest",
    "transaction_id": "txn123",
    "amount": 100.0,
    "currency": "USD",
    "category": "test",
    "type": "expense",
    "date": "2025-03-27T12:00:00Z",
    "notes": "Initial test insert"
}'

GET:

curl http://localhost:8000/api/v1/transaction/loadtest/txn123

DELETE:

curl -X DELETE http://localhost:8000/api/v1/transaction/loadtest/txn123

///////////////////////////////////////////////////////////////////////////////////////////////

Package:

Robert@DESKTOP-6B38QOU MINGW64 /c/Projects/Python
$ tar -czf fastapi_app.tar.gz FastAPI

Move to server:

Robert@DESKTOP-6B38QOU MINGW64 /c/Projects/Python
$ scp fastapi_app.tar.gz rob@master:/home/rob/
rob@master's password: 
fastapi_app.tar.gz      