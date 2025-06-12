echo "Starting Backend..."
source venv/bin/activate
cd backend
pip install -r "requirements.txt"
python3 main.py &
cd ..
echo "Starting Frontend..."
cd frontend
npm run dev

kill %1
