import pandas as pd
from typing import Dict, List, Any
from collections import Counter


class AnalyticsService:

    @staticmethod
    def generate_insights(df: pd.DataFrame) -> Dict[str, Any]:
        insights = {}
        if 'views' in df.columns:
            insights['total_views'] = int(df['views'].sum())
            insights['average_views'] = float(df['views'].mean())

        if 'watch_time' in df.columns:
            insights['total_watch_time'] = float(df['watch_time'].sum())
            insights['average_watch_time'] = float(df['watch_time'].mean())

        if 'country' in df.columns:
            country_views = df.groupby('country')['views'].sum().sort_values(ascending=False)
            insights['top_countries'] = country_views.head(10).to_dict()

        if 'age_group' in df.columns:
            age_dist = df['age_group'].value_counts().to_dict()
            insights['age_distribution'] = age_dist

        if 'device_type' in df.columns:
            device_dist = df['device_type'].value_counts().to_dict()
            insights['device_breakdown'] = device_dist

        if 'gender' in df.columns:
            gender_dist = df['gender'].value_counts().to_dict()
            insights['gender_distribution'] = gender_dist

        return insights

    @staticmethod
    def prepare_chart_data(df: pd.DataFrame, chart_type: str, column: str) -> Dict[str, Any]:

        if chart_type == "bar" and column in df.columns:
            data_counts = df[column].value_counts()
            return {
                "labels": data_counts.index.tolist(),
                "datasets": [{
                    "label": f"{column.replace('_', ' ').title()} Distribution",
                    "data": data_counts.values.tolist(),
                    "backgroundColor": [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 205, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)'
                    ],
                    "borderColor": [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 205, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    "borderWidth": 1
                }]
            }

        elif chart_type == "pie" and column in df.columns:
            data_counts = df[column].value_counts()
            return {
                "labels": data_counts.index.tolist(),
                "datasets": [{
                    "data": data_counts.values.tolist(),
                    "backgroundColor": [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#FF6384', '#C9CBCF'
                    ]
                }]
            }

        elif chart_type == "line" and 'date' in df.columns and column in df.columns:
            # Time series data
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            time_series = df.groupby('date')[column].sum().sort_index()

            return {
                "labels": [date.strftime('%Y-%m-%d') for date in time_series.index],
                "datasets": [{
                    "label": f"{column.replace('_', ' ').title()} Over Time",
                    "data": time_series.values.tolist(),
                    "borderColor": 'rgba(75, 192, 192, 1)',
                    "backgroundColor": 'rgba(75, 192, 192, 0.2)',
                    "tension": 0.1
                }]
            }

        return {"labels": [], "datasets": []}
