class APIClient {
    constructor() {
        this.baseURL = 'http://localhost:8000/api/v1';
    }

    async uploadCSV(file) {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${this.baseURL}/upload-csv`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }

        return await response.json();
    }

    async getAnalytics(fileId) {
        const response = await fetch(`${this.baseURL}/analytics/${fileId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch analytics');
        }

        return await response.json();
    }

    async getChartData(fileId, chartType, column) {
        const response = await fetch(
            `${this.baseURL}/chart-data/${fileId}?chart_type=${chartType}&column=${column}`
        );
        
        if (!response.ok) {
            throw new Error('Failed to fetch chart data');
        }

        return await response.json();
    }

    async getColumns(fileId) {
        const response = await fetch(`${this.baseURL}/columns/${fileId}`);
        
        if (!response.ok) {
            throw new Error('Failed to fetch columns');
        }

        return await response.json();
    }
}

const apiClient = new APIClient();
