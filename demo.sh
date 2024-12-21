# python3 -m venv venv
# source venv/bin/activate # mac/linux
pip install -r requirements.txt
python3 ./server/server.py &
SERVER_PID=$!

python3 ./client/main.py

sleep 3
kill $SERVER_PID