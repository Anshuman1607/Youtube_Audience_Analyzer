class ChartManager {
    constructor() {
        this.currentChart = null;
        this.chartContainer = document.getElementById('mainChart');
    }

    createChart(data, type) {
        
        if (this.currentChart) {
            this.currentChart.destroy();
        }

        const ctx = this.chartContainer.getContext('2d');
        
        const config = {
            type: type,
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: `${data.datasets[0].label || 'Data Visualization'}`
                    }
                }
            }
        };

        if (type === 'bar') {
            config.options.scales = {
                y: {
                    beginAtZero: true
                }
            };
        } else if (type === 'line') {
            config.options.scales = {
                x: {
                    display: true
                },
                y: {
                    beginAtZero: true
                }
            };
            config.options.elements = {
                line: {
                    tension: 0.1
                }
            };
        } else if (type === 'pie' || type === 'doughnut') {
            config.options.plugins.legend.position = 'right';
        }

        this.currentChart = new Chart(ctx, config);
    }

    updateChart(data, type) {
        this.createChart(data, type);
    }

    clearChart() {
        if (this.currentChart) {
            this.currentChart.destroy();
            this.currentChart = null;
        }
    }
}

const chartManager = new ChartManager();
