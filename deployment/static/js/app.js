// Temenos RAG AI Web Application JavaScript
class TemenosRAGApp {
    constructor() {
        this.apiBase = '/api';
        this.selectedPillars = new Set();
        this.currentAnalysis = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadPillars();
        this.testConnection();
        this.loadHistory();
        this.loadReports();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.dataset.section;
                this.showSection(section);
            });
        });

        // Form submission
        document.getElementById('analysisForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.startAnalysis();
        });

        // Buttons
        document.getElementById('testConnectionBtn').addEventListener('click', () => {
            this.testConnection();
        });

        document.getElementById('batchAnalyzeBtn').addEventListener('click', () => {
            this.startBatchAnalysis();
        });

        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.refreshData();
        });

        document.getElementById('infoBtn').addEventListener('click', () => {
            this.showModal('infoModal');
        });

        // Modal close
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.hideModal(e.target.closest('.modal'));
            });
        });

        // Close modal on outside click
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal);
                }
            });
        });
    }

    showSection(sectionName) {
        // Update navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Show content section
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });

        switch(sectionName) {
            case 'dashboard':
                document.getElementById('dashboard-section').classList.add('active');
                break;
            case 'history':
                document.getElementById('history-section').classList.add('active');
                this.loadHistory();
                break;
            case 'reports':
                document.getElementById('reports-section').classList.add('active');
                this.loadReports();
                break;
        }
    }

    async loadPillars() {
        try {
            const response = await fetch(`${this.apiBase}/pillars`);
            const data = await response.json();
            
            if (data.pillars) {
                this.renderPillars(data.pillars);
            }
        } catch (error) {
            console.error('Error loading pillars:', error);
            this.showMessage('Error loading pillars', 'error');
        }
    }

    renderPillars(pillars) {
        const grid = document.getElementById('pillarsGrid');
        grid.innerHTML = '';

        pillars.forEach(pillar => {
            const pillarItem = document.createElement('div');
            pillarItem.className = 'pillar-item';
            pillarItem.dataset.pillar = pillar;
            pillarItem.innerHTML = `
                <h4>${pillar}</h4>
                <p>Technology Analysis</p>
            `;
            
            pillarItem.addEventListener('click', () => {
                this.togglePillar(pillar, pillarItem);
            });
            
            grid.appendChild(pillarItem);
        });
    }

    togglePillar(pillar, element) {
        if (this.selectedPillars.has(pillar)) {
            this.selectedPillars.delete(pillar);
            element.classList.remove('selected');
        } else {
            this.selectedPillars.add(pillar);
            element.classList.add('selected');
        }
    }

    async testConnection() {
        const btn = document.getElementById('testConnectionBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="loading"></div> Testing...';
        btn.disabled = true;

        try {
            const response = await fetch(`${this.apiBase}/test-connection`);
            const data = await response.json();
            
            this.updateConnectionStatus(data.connected);
            
            if (data.connected) {
                this.showMessage('Connection successful!', 'success');
            } else {
                this.showMessage('Connection failed. Please check your configuration.', 'error');
            }
        } catch (error) {
            console.error('Connection test failed:', error);
            this.updateConnectionStatus(false);
            this.showMessage('Connection test failed', 'error');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connectionStatus');
        const icon = statusElement.querySelector('i');
        
        if (connected) {
            statusElement.className = 'status-indicator connected';
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Connected';
        } else {
            statusElement.className = 'status-indicator disconnected';
            statusElement.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
        }
    }

    async startAnalysis() {
        if (this.selectedPillars.size === 0) {
            this.showMessage('Please select at least one pillar to analyze', 'warning');
            return;
        }

        const formData = new FormData(document.getElementById('analysisForm'));
        const analysisData = {
            region: formData.get('region'),
            model_id: 'TechnologyOverview',
            product_name: formData.get('product'),
            pillar: Array.from(this.selectedPillars)[0] // For single analysis
        };

        this.showProgress();
        this.updateProgress(0, 'Starting analysis...');

        try {
            const response = await fetch(`${this.apiBase}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(analysisData)
            });

            const data = await response.json();

            if (data.success) {
                this.updateProgress(100, 'Analysis completed!');
                this.showResults([data.analysis]);
                this.showMessage('Analysis completed successfully!', 'success');
            } else {
                throw new Error(data.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Analysis failed:', error);
            this.hideProgress();
            this.showMessage(`Analysis failed: ${error.message}`, 'error');
        }
    }

    async startBatchAnalysis() {
        if (this.selectedPillars.size === 0) {
            this.showMessage('Please select pillars to analyze', 'warning');
            return;
        }

        const formData = new FormData(document.getElementById('analysisForm'));
        const analysisData = {
            region: formData.get('region'),
            model_id: 'TechnologyOverview',
            product_name: formData.get('product'),
            pillars: Array.from(this.selectedPillars)
        };

        this.showProgress();
        this.updateProgress(0, 'Starting batch analysis...');

        try {
            const response = await fetch(`${this.apiBase}/batch-analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(analysisData)
            });

            const data = await response.json();

            if (data.success) {
                this.updateProgress(100, 'Batch analysis completed!');
                this.showBatchResults(data.results);
                this.showMessage(`Batch analysis completed: ${data.summary.successful}/${data.summary.total} successful`, 'success');
            } else {
                throw new Error(data.error || 'Batch analysis failed');
            }
        } catch (error) {
            console.error('Batch analysis failed:', error);
            this.hideProgress();
            this.showMessage(`Batch analysis failed: ${error.message}`, 'error');
        }
    }

    showProgress() {
        document.getElementById('progressSection').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
    }

    hideProgress() {
        document.getElementById('progressSection').style.display = 'none';
    }

    updateProgress(percentage, text) {
        document.getElementById('progressFill').style.width = `${percentage}%`;
        document.getElementById('progressText').textContent = text;
        document.getElementById('progressDetails').textContent = `Progress: ${percentage}%`;
    }

    showResults(results) {
        this.hideProgress();
        const resultsSection = document.getElementById('resultsSection');
        const resultsTable = document.getElementById('resultsTable');
        
        resultsSection.style.display = 'block';
        
        resultsTable.innerHTML = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Pillar</th>
                        <th>Product</th>
                        <th>Region</th>
                        <th>Questions</th>
                        <th>Key Points</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(result => `
                        <tr>
                            <td>${result.pillar}</td>
                            <td>${result.product}</td>
                            <td>${result.region}</td>
                            <td>${result.questions_asked.length}</td>
                            <td>${result.key_points.length}</td>
                            <td>
                                <button class="btn btn-secondary" onclick="app.downloadAnalysis('${result.pillar}')">
                                    <i class="fas fa-download"></i> Download
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    showBatchResults(results) {
        this.hideProgress();
        const resultsSection = document.getElementById('resultsSection');
        const resultsTable = document.getElementById('resultsTable');
        
        resultsSection.style.display = 'block';
        
        resultsTable.innerHTML = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Pillar</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(result => `
                        <tr>
                            <td>${result.pillar}</td>
                            <td>
                                <span class="status-indicator ${result.success ? 'connected' : 'disconnected'}">
                                    <i class="fas fa-circle"></i> ${result.success ? 'Success' : 'Failed'}
                                </span>
                            </td>
                            <td>
                                ${result.success ? `
                                    <button class="btn btn-secondary" onclick="app.downloadAnalysis('${result.pillar}')">
                                        <i class="fas fa-download"></i> Download
                                    </button>
                                ` : `
                                    <span class="error">${result.error}</span>
                                `}
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async downloadAnalysis(pillar) {
        try {
            // This would typically generate and download the Word document
            this.showMessage(`Downloading ${pillar} analysis...`, 'success');
        } catch (error) {
            console.error('Download failed:', error);
            this.showMessage('Download failed', 'error');
        }
    }

    async loadHistory() {
        try {
            const response = await fetch(`${this.apiBase}/reports`);
            const data = await response.json();
            
            if (data.reports) {
                this.renderHistory(data.reports);
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    renderHistory(reports) {
        const historyTable = document.getElementById('historyTable');
        
        if (reports.length === 0) {
            historyTable.innerHTML = '<p>No analysis history found.</p>';
            return;
        }

        historyTable.innerHTML = `
            <table class="table">
                <thead>
                    <tr>
                        <th>Filename</th>
                        <th>Size</th>
                        <th>Created</th>
                        <th>Modified</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${reports.map(report => `
                        <tr>
                            <td>${report.filename}</td>
                            <td>${this.formatFileSize(report.size)}</td>
                            <td>${new Date(report.created).toLocaleString()}</td>
                            <td>${new Date(report.modified).toLocaleString()}</td>
                            <td>
                                <button class="btn btn-secondary" onclick="app.downloadFile('${report.filename}')">
                                    <i class="fas fa-download"></i> Download
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadReports() {
        try {
            const response = await fetch(`${this.apiBase}/word-documents`);
            const data = await response.json();
            
            if (data.documents) {
                this.renderReports(data.documents);
            }
        } catch (error) {
            console.error('Error loading reports:', error);
        }
    }

    renderReports(documents) {
        const reportsGrid = document.getElementById('reportsGrid');
        
        if (documents.length === 0) {
            reportsGrid.innerHTML = '<p>No Word documents found.</p>';
            return;
        }

        reportsGrid.innerHTML = `
            <div class="reports-list">
                ${documents.map(doc => `
                    <div class="report-item">
                        <div class="report-info">
                            <h4>${doc.filename}</h4>
                            <p>Size: ${this.formatFileSize(doc.size)}</p>
                            <p>Modified: ${new Date(doc.modified).toLocaleString()}</p>
                        </div>
                        <div class="report-actions">
                            <button class="btn btn-primary" onclick="app.downloadFile('${doc.filename}')">
                                <i class="fas fa-download"></i> Download
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    async downloadFile(filename) {
        try {
            const response = await fetch(`${this.apiBase}/download/${filename}`);
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                this.showMessage(`Downloaded ${filename}`, 'success');
            } else {
                throw new Error('Download failed');
            }
        } catch (error) {
            console.error('Download failed:', error);
            this.showMessage('Download failed', 'error');
        }
    }

    async refreshData() {
        this.loadHistory();
        this.loadReports();
        this.testConnection();
        this.showMessage('Data refreshed', 'success');
    }

    showModal(modalId) {
        document.getElementById(modalId).classList.add('active');
    }

    hideModal(modal) {
        modal.classList.remove('active');
    }

    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = message;
        
        // Insert at the top of the content area
        const contentArea = document.querySelector('.content-area');
        contentArea.insertBefore(messageDiv, contentArea.firstChild);
        
        // Remove after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.parentNode.removeChild(messageDiv);
            }
        }, 5000);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Initialize the application
const app = new TemenosRAGApp();
