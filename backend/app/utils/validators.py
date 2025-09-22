import pandas as pd
from typing import List, Dict, Any
import re


class YouTubeDataValidator:

    @staticmethod
    def validate_csv_structure(df: pd.DataFrame) -> Dict[str, Any]:
        """Validate the structure of uploaded CSV"""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "summary": {}
        }

        if df.empty:
            validation_result["is_valid"] = False
            validation_result["errors"].append("CSV file is empty")
            return validation_result
        expected_columns = [
            'views', 'watch_time', 'country', 'age_group',
            'gender', 'device_type', 'traffic_source'
        ]

        missing_columns = [col for col in expected_columns if col not in df.columns]
        if missing_columns:
            validation_result["warnings"].append(f"Missing optional columns: {missing_columns}")

        numeric_columns = ['views', 'watch_time']
        for col in numeric_columns:
            if col in df.columns:
                if not pd.api.types.is_numeric_dtype(df[col]):
                    try:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                    except ValueError:
                        validation_result["errors"].append(f"Column {col} should be numeric")

        missing_data = df.isnull().sum()
        if missing_data.sum() > 0:
            validation_result["warnings"].append(f"Missing values found: {missing_data.to_dict()}")


        if 'views' in df.columns:
            negative_views = (df['views'] < 0).sum()
            if negative_views > 0:
                validation_result["errors"].append(f"Found {negative_views} negative view counts")

        validation_result["summary"] = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "columns": list(df.columns)
        }

        return validation_result

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:

        df = df.dropna(how='all')

        numeric_columns = df.select_dtypes(include=['number']).columns
        df[numeric_columns] = df[numeric_columns].fillna(0)

        categorical_columns = df.select_dtypes(include=['object']).columns
        df[categorical_columns] = df[categorical_columns].fillna('Unknown')

        return df