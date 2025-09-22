# YouTube Audience Analyzer

A full-stack web app for visualizing YouTube audience data. Upload analytics CSV files to get instant insights, interactive charts, and summary stats—ideal for creators and marketers. Built with FastAPI (Python), Pandas, Chart.js, HTML, CSS, and JavaScript.

## Features
- Upload and analyze YouTube CSV data
- Dashboard with summary cards and preview table
- Dynamic charts: age, country, gender, device, trends

## Tech Stack
- **Backend:** FastAPI, Python, Pandas
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **API:** REST (JSON)

## Getting Started
1. Clone the repo:
    ```
    git clone https://github.com/yourusername/youtube-audience-analyzer.git
    ```

2. Install backend dependencies:
    ```
    cd backend
    pip install -r requirements.txt
    python run.py
    ```

3. Serve the frontend:
    ```
    cd frontend
    python -m http.server 3000
    ```

4. Open `http://localhost:3000` in your browser and upload your CSV file!
