from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import pandas as pd
from typing import Dict, Any

from ..services.csv_processor import CSVProcessor
from ..services.analytics_service import AnalyticsService
from ..utils.validators import YouTubeDataValidator
from ..core.config import settings

router = APIRouter()

# Store processed data temporarily (in production, use a database)
processed_data_store = {}


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    contents = await file.read()
    if len(contents) > settings.max_file_size:
        raise HTTPException(status_code=400, detail="File too large")

    await file.seek(0)

    try:
        df = await CSVProcessor.process_upload_file(file)

        validation_result = YouTubeDataValidator.validate_csv_structure(df)

        if not validation_result["is_valid"]:
            raise HTTPException(status_code=400, detail=validation_result["errors"])

        df_cleaned = YouTubeDataValidator.clean_data(df)

        file_id = f"file_{len(processed_data_store)}"
        processed_data_store[file_id] = df_cleaned

        return JSONResponse(content={
            "message": "File uploaded and processed successfully",
            "file_id": file_id,
            "filename": file.filename,
            "rows_processed": len(df_cleaned),
            "columns": list(df_cleaned.columns),
            "validation_warnings": validation_result.get("warnings", []),
            "summary": validation_result["summary"]
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/{file_id}")
async def get_analytics(file_id: str):

    if file_id not in processed_data_store:
        raise HTTPException(status_code=404, detail="File not found")

    df = processed_data_store[file_id]
    insights = AnalyticsService.generate_insights(df)

    return JSONResponse(content=insights)


@router.get("/chart-data/{file_id}")
async def get_chart_data(file_id: str, chart_type: str, column: str):

    if file_id not in processed_data_store:
        raise HTTPException(status_code=404, detail="File not found")

    df = processed_data_store[file_id]

    if column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{column}' not found")

    chart_data = AnalyticsService.prepare_chart_data(df, chart_type, column)

    return JSONResponse(content=chart_data)


@router.get("/columns/{file_id}")
async def get_columns(file_id: str):

    if file_id not in processed_data_store:
        raise HTTPException(status_code=404, detail="File not found")

    df = processed_data_store[file_id]

    return JSONResponse(content={
        "columns": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "sample_data": df.head(5).to_dict('records')
    })
