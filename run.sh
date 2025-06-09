pip install -r requirements.txt

echo "Starting Backend..."
source venv/bin/activate
python3 main.py &

echo "Starting Frontend..."
cd frontend
npm run dev

kill %1
