echo "Starting Backend..."
source venv/bin/activate
pip install -r "requirements.txt"
python3 main.py &

echo "Starting Frontend..."
cd frontend
npm run dev

kill %1
