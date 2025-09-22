# YouTube Audience Analyzer

YouTube Audience Analyzer is a full-stack web app that enables creators, marketers, and data enthusiasts to upload YouTube analytics CSV files and instantly visualize audience data through interactive dashboards and charts.

# Features
Upload and analyze YouTube audience CSV data

Automatically validates, cleans, and summarizes input

Interactive visualizations: age, country, device, gender, watch time trends

Responsive dashboard built with Chart.js

Tech Stack
Backend: FastAPI, Python, Pandas

Frontend: HTML, CSS, JavaScript, Chart.js

Data Handling: CSV file upload & REST API

Getting Started
Clone the repo:
git clone https://github.com/yourusername/youtube-audience-analyzer.git
Install backend dependencies:

bash
cd backend
pip install -r requirements.txt
Run the backend:

bash
python run.py
Serve the frontend:

bash
cd frontend
python -m http.server 3000
Visit http://localhost:3000, upload a CSV, and explore your analytics!
