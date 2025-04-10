start for windows:
uvicorn app.main:app --reload 

start for ubuntu:
gunicorn app.main:app -k uvicorn.workers.UvicornWorker -w 4 --bind 0.0.0.0:8000

source venv/bin/activate


///////////////////////////////////////////////////////////////////////////////////////////////

apache benchmark load_test:
ab -n 100 -c 10 http://localhost:8000/api/v1/transaction/loadtest/txn123

///////////////////////////////////////////////////////////////////////////////////////////////

CRUD examples:

POST:

curl -X POST http://localhost:30080/api/v1/transaction/ \
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

//////////////////////////////////////////////////////////////////////////////////////////////

helm:


helm repo add fastapi https://rhadaway14.github.io/fast-app-helm
helm repo update

helm install fastapi-app fastapi/fastapi-app \
  --set couchbase.host=couchbase://3.139.85.71 \
  --set couchbase.bucket=Fin \
  --set couchbase.scope=money \
  --set couchbase.collection=transactions \
  --set couchbase.user=Administrator \
  --set couchbase.password=password \
  --set workers=4





curl -X POST http://ec2-3-139-85-71.us-east-2.compute.amazonaws.com:30080/api/v1/transaction/ \
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



http://ec2-3-148-194-247.us-east-2.compute.amazonaws.com:30080/api/v1/transaction/loadtest/txn123


ab -n 10000 -c 10 http://ec2-3-148-194-247.us-east-2.compute.amazonaws.com:30080/api/v1/transaction/loadtest/txn123

wrk -t8 -c100 -d30s http://ec2-3-148-194-247.us-east-2.compute.amazonaws.com:31379/api/v1/transaction/loadtest/txn123


helm repo add fastapi https://rhadaway14.github.io/fast-app-helm

helm install fastapi-app fastapi/fastapi-app \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=16 \
  --set autoscaling.maxReplicas=20 \
  --set autoscaling.targetCPUUtilizationPercentage=60 \
  --set autoscaling.targetMemoryUtilizationPercentage=70 \
  --set workers=4 \
  --set couchbase.host="couchbase://10.0.15.63" \
  --set couchbase.bucket="Fin" \
  --set couchbase.scope="money" \
  --set couchbase.collection="transactions" \
  --set couchbase.user="Administrator" \
  --set couchbase.password="password"



testing script:

#!/bin/bash

ab -n 1000 -c 1 http://10.0.10.48/api/v1/transaction/perftest/loadtest/txn123
wrk -t16 -c400 -d30s http://10.0.10.48/api/v1/transaction/perftest/loadtest/txn123

#wrk -t16 -c400 -d30s -s ./report.lua http://10.0.10.48/api/v1/transaction/perftest/loadtest/txn123


HAProxy

sudo dnf install -y haproxy
sudo nano /etc/haproxy/haproxy.cfg



global
    log /dev/log local0
    log /dev/log local1 notice
    daemon
    maxconn 10000

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  http-server-close
    option  forwardfor except 127.0.0.0/8
    option  redispatch
    retries 3
    timeout connect 10s
    timeout client  1m
    timeout server  1m
    timeout http-request 10s
    timeout http-keep-alive 10s
    timeout queue 1m
    timeout check 10s
    maxconn 10000

frontend http_front
    bind *:80
    default_backend fastapi_back
    option http-server-close
    option forwardfor
    http-request set-header Connection keep-alive

backend fastapi_back
    balance roundrobin
    option httpchk GET /api/v1/healthz
    http-check expect status 200
    option http-keep-alive
    http-reuse always
    http-response set-header Connection keep-alive
    server k8s-node-1 10.0.4.168:30080 check
    server k8s-node-2 10.0.6.170:30080 check
    server k8s-node-3 10.0.6.219:30080 check
    server k8s-node-4 10.0.11.60:30080 check
    server k8s-node-5 10.0.13.148:30080 check
    


//////////////////////

sudo systemctl enable haproxy
sudo systemctl restart haproxy



