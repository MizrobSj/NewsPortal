Description: 
A real-time news portal app built with FastAPI and SocketIO(python-socketio). This app includes an admin endpoint for automatically generating news.

How To Run the Project:
1) Create a virtual environment
 python -m venv venv  
2) Activate a virtual environment
 venv\Scripts\activate  --- for Windows
 source venv/bin/activate --- for macOS
3) Install all dependencies from requirments.txt
 pip install -r requirements.txt
4) Run the FastAPI server by using Uvicorn
 uvicorn app.main:app --reload
5) Open in your browser client page
  http://localhost:8000
6) Generate first news from terminal using by curl
   curl -X POST http://localhost:8000/admin/generate_news
7) Start auto generation of news
  curl -X POST "http://localhost:8000/admin/start_auto_generate?interval_seconds=10"
8) Stop auto generation of news
  curl -X POST http://localhost:8000/admin/stop_auto_generate
  
