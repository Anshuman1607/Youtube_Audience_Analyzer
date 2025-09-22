class YouTubeAnalyzer {
    constructor() {
        this.currentFileId = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // File upload elements
        const uploadArea = document.getElementById('uploadArea');
        const csvFile = document.getElementById('csvFile');
        const browseBtn = document.getElementById('browseBtn');
        
        // Chart controls
        const generateChartBtn = document.getElementById('generateChart');
        
        // Browse button click
        browseBtn.addEventListener('click', () => csvFile.click());
        
        // File input change
        csvFile.addEventListener('change', (e) => this.handleFileSelect(e.target.files[0]));
        
        // Drag and drop
        uploadArea.addEventListener('click', () => csvFile.click());
        uploadArea.addEventListener('dragover', this.handleDragOver);
        uploadArea.addEventListener('dragleave', this.handleDragLeave);
        uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        
        // Chart generation
        generateChartBtn.addEventListener('click', this.generateChart.bind(this));
    }

    handleDragOver(e) {
        e.preventDefault();
        e.currentTarget.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            this.handleFileSelect(files[0]);
        }
    }

    async handleFileSelect(file) {
        if (!file || !file.name.endsWith('.csv')) {
            this.showUploadStatus('Please select a valid CSV file.', 'error');
            return;
        }

        this.showUploadStatus('Uploading and processing file...', 'loading');

        try {
            const result = await apiClient.uploadCSV(file);
            this.currentFileId = result.file_id;
            
            this.showUploadStatus(
                `✅ ${result.message} (${result.rows_processed} rows processed)`, 
                'success'
            );
            
            await this.loadAnalytics();
            await this.loadColumns();
            this.showDashboard();
            
        } catch (error) {
            this.showUploadStatus(`❌ Error: ${error.message}`, 'error');
        }
    }

    showUploadStatus(message, type) {
        const statusDiv = document.getElementById('uploadStatus');
        statusDiv.innerHTML = type === 'loading' ? 
            `<div class="loading"></div> ${message}` : message;
        statusDiv.className = `upload-status ${type}`;
        statusDiv.style.display = 'block';
        
        if (type === 'success') {
            setTimeout(() => {
                statusDiv.style.display = 'none';
            }, 3000);
        }
    }

    async loadAnalytics() {
        try {
            const analytics = await apiClient.getAnalytics(this.currentFileId);
            this.updateSummaryCards(analytics);
        } catch (error) {
            console.error('Error loading analytics:', error);
        }
    }

    async loadColumns() {
        try {
            const columnData = await apiClient.getColumns(this.currentFileId);
            this.populateColumnSelect(columnData.columns);
            this.updateDataPreview(columnData.sample_data);
        } catch (error) {
            console.error('Error loading columns:', error);
        }
    }

    updateSummaryCards(analytics) {
        document.getElementById('totalViews').textContent = 
            this.formatNumber(analytics.total_views || 0);
        document.getElementById('totalWatchTime').textContent = 
            this.formatNumber(analytics.total_watch_time || 0);
        document.getElementById('avgViewDuration').textContent = 
            this.formatDuration(analytics.average_watch_time || 0);
        
        const topCountry = analytics.top_countries ? 
            Object.keys(analytics.top_countries)[0] : 'N/A';
        document.getElementById('topCountry').textContent = topCountry;
    }

    populateColumnSelect(columns) {
        const select = document.getElementById('dataColumn');
        select.innerHTML = '<option value="">Select a column...</option>';
        
        columns.forEach(column => {
            const option = document.createElement('option');
            option.value = column;
            option.textContent = column.replace('_', ' ').toUpperCase();
            select.appendChild(option);
        });
    }

    updateDataPreview(sampleData) {
        const table = document.getElementById('dataTable');
        const thead = table.querySelector('thead');
        const tbody = table.querySelector('tbody');
        
        if (sampleData.length === 0) return;
        
        thead.innerHTML = '';
        const headerRow = document.createElement('tr');
        Object.keys(sampleData[0]).forEach(key => {
            const th = document.createElement('th');
            th.textContent = key.replace('_', ' ').toUpperCase();
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        
        tbody.innerHTML = '';
        sampleData.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
    }

    async generateChart() {
        const chartType = document.getElementById('chartType').value;
        const column = document.getElementById('dataColumn').value;
        
        if (!column) {
            alert('Please select a data column');
            return;
        }
        
        try {
            const chartData = await apiClient.getChartData(this.currentFileId, chartType, column);
            chartManager.createChart(chartData, chartType);
        } catch (error) {
            alert(`Error generating chart: ${error.message}`);
        }
    }

    showDashboard() {
        document.getElementById('dashboard').style.display = 'block';
        document.getElementById('dashboard').scrollIntoView({ behavior: 'smooth' });
    }

    formatNumber(num) {
        return new Intl.NumberFormat().format(Math.round(num));
    }

    formatDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new YouTubeAnalyzer();
});
