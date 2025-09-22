import pandas as pd
import csv
from io import StringIO
from fastapi import UploadFile, HTTPException
from typing import Dict, Any
import os


class CSVProcessor:

    @staticmethod
    async def process_upload_file(file: UploadFile) -> pd.DataFrame:
        try:
            contents = await file.read()

            csv_string = contents.decode('utf-8')

            buffer = StringIO(csv_string)

            df = pd.read_csv(buffer)

            return df

        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8.")
        except pd.errors.EmptyDataError:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        except pd.errors.ParserError as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

    @staticmethod
    def save_processed_data(df: pd.DataFrame, filename: str, upload_dir: str) -> str:
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, f"processed_{filename}")
        df.to_csv(file_path, index=False)
        return file_path
