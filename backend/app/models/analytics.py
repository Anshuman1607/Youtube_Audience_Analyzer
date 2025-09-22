from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class CSVUploadResponse(BaseModel):
    message: str
    filename: str
    rows_processed: int
    columns: List[str]

class AnalyticsInsights(BaseModel):
    total_views: int
    total_watch_time: float
    average_view_duration: float
    top_countries: Dict[str, int]
    age_distribution: Dict[str, int]
    device_breakdown: Dict[str, int]
    gender_distribution: Dict[str, int]
    peak_watch_times: Dict[str, int]

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]
    chart_type: str