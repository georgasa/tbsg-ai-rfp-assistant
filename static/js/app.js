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

        document.getElementById('clearHistoryBtn').addEventListener('click', () => {
            this.clearHistory();
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
        const activeItem = document.querySelector(`[data-section="${sectionName}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }

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
            case 'favorites':
                // Favorites functionality - placeholder
                document.getElementById('dashboard-section').classList.add('active');
                break;
            default:
                // Default to dashboard for any non-functional sections
                document.getElementById('dashboard-section').classList.add('active');
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
                this.showMessage('RAG API connection successful!', 'success');
            } else {
                this.showMessage('RAG API is not available. Analysis will not work.', 'error');
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
        const selectedProducts = Array.from(document.getElementById('products').selectedOptions).map(option => option.value);
        
        if (selectedProducts.length === 0) {
            this.showMessage('Please select at least one product', 'warning');
            return;
        }
        
        const analysisData = {
            region: formData.get('region'),
            model_id: 'TechnologyOverview', // Will be mapped on server side
            products: selectedProducts,
            pillar: Array.from(this.selectedPillars)[0] // For single analysis
        };

        this.showProgress();
        this.updateProgress(5, 'Initializing analysis...');

        try {
            // Simulate progress updates during analysis
            let currentProgress = 5;
            const progressInterval = setInterval(() => {
                if (currentProgress < 90) {
                    currentProgress = Math.min(currentProgress + Math.random() * 10 + 5, 90);
                    this.updateProgress(Math.round(currentProgress), `Analyzing ${selectedProducts.join(', ')}...`);
                }
            }, 1000);
            
            const response = await fetch(`${this.apiBase}/analyze`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(analysisData)
            });

            clearInterval(progressInterval);
            this.updateProgress(95, 'Generating Word document...');
            
            const data = await response.json();

            if (data.success) {
                this.updateProgress(100, 'Analysis completed!');
                
                // Handle combined analysis results
                if (data.combined_analysis) {
                    this.showCombinedResults(data);
                    this.showMessage(`Combined analysis completed for ${data.combined_analysis.products.length} product(s)!`, 'success');
                } else if (data.results && data.results.length > 0) {
                    this.showResults(data.results);
                    this.showMessage(`Analysis completed for ${data.results.length} product(s)!`, 'success');
                } else {
                    this.showResults([data.analysis]);
                    this.showMessage('Analysis completed successfully!', 'success');
                }
            } else {
                // Handle API not available error
                if (response.status === 503) {
                    this.showMessage('RAG API is not available. Please check your connection and try again.', 'error');
                } else {
                    throw new Error(data.error || 'Analysis failed');
                }
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
        const selectedProducts = Array.from(document.getElementById('products').selectedOptions).map(option => option.value);
        
        if (selectedProducts.length === 0) {
            this.showMessage('Please select at least one product', 'warning');
            return;
        }
        
        const analysisData = {
            region: formData.get('region'),
            model_id: 'TechnologyOverview', // Will be mapped on server side
            products: selectedProducts,
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
                this.currentAnalysis = data; // Store results for download functionality
                this.showBatchResults(data.results);
                this.showMessage(`Batch analysis completed: ${data.summary.successful}/${data.summary.total} successful`, 'success');
            } else {
                // Handle API not available error
                if (response.status === 503) {
                    this.showMessage('RAG API is not available. Please check your connection and try again.', 'error');
                } else {
                    throw new Error(data.error || 'Batch analysis failed');
                }
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
                        <th>Date/Time</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${results.map(result => {
                        const analysis = result.analysis || result;
                        return `
                        <tr>
                            <td>${result.pillar || analysis.pillar || 'Unknown'}</td>
                            <td>${result.product || analysis.product || 'Unknown'}</td>
                            <td>${result.region || analysis.region || 'Unknown'}</td>
                            <td>${analysis.questions_asked ? analysis.questions_asked.length : 0}</td>
                            <td>${analysis.key_points ? analysis.key_points.length : 0}</td>
                            <td>${analysis.timestamp ? new Date(analysis.timestamp).toLocaleString() : 'Unknown'}</td>
                            <td>
                                ${result.word_filename || result.word_filepath ? `
                                    <button class="btn btn-success" onclick="app.downloadWord('${result.word_filename || result.word_filepath}')">
                                        <i class="fas fa-file-word"></i> Download Word
                                    </button>
                                ` : `
                                    <button class="btn btn-primary" onclick="app.generateAndDownloadWord('${result.filepath}', '${result.product || analysis.product}', '${result.pillar || analysis.pillar}')">
                                        <i class="fas fa-file-word"></i> Generate Word
                                    </button>
                                `}
                            </td>
                        </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;
    }

    showCombinedResults(data) {
        this.hideProgress();
        const resultsSection = document.getElementById('resultsSection');
        const resultsTable = document.getElementById('resultsTable');
        
        if (!resultsSection || !resultsTable) {
            console.error('Results section or table not found');
            return;
        }
        
        resultsSection.style.display = 'block';
        
        const combinedAnalysis = data.combined_analysis;
        const products = combinedAnalysis.products.join(', ');
        
        resultsTable.innerHTML = `
            <div class="combined-results-header">
                <h3>Combined Analysis Results</h3>
                <p><strong>Products:</strong> ${products}</p>
                <p><strong>Pillar:</strong> ${combinedAnalysis.pillar}</p>
                <p><strong>Region:</strong> ${combinedAnalysis.region}</p>
                <p><strong>Total Key Points:</strong> ${combinedAnalysis.combined_key_points.length}</p>
                <p><strong>Generated:</strong> ${new Date(combinedAnalysis.timestamp).toLocaleString()}</p>
            </div>
            <div class="combined-actions">
                ${data.word_filename ? `
                    <button class="btn btn-success btn-lg" onclick="app.downloadWord('${data.word_filename}')">
                        <i class="fas fa-file-word"></i> Download Combined Word Document
                    </button>
                ` : `
                    <button class="btn btn-primary btn-lg" onclick="app.generateAndDownloadCombinedWord('${data.filepath}', '${products}', '${combinedAnalysis.pillar}')">
                        <i class="fas fa-file-word"></i> Generate Combined Word Document
                    </button>
                `}
            </div>
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
            this.showMessage(`Downloading ${pillar} analysis...`, 'info');
            
            // Get the word document filename from the results
            const results = this.currentAnalysis?.results || [];
            const result = results.find(r => r.pillar === pillar);
            
            if (result && result.word_filename) {
                // Download the Word document
                const response = await fetch(`${this.apiBase}/download/${result.word_filename}`);
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = result.word_filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    this.showMessage(`Downloaded ${pillar} analysis successfully!`, 'success');
                } else {
                    throw new Error('Download failed');
                }
            } else {
                throw new Error('No document available for download');
            }
        } catch (error) {
            console.error('Download failed:', error);
            this.showMessage(`Download failed for ${pillar}: ${error.message}`, 'error');
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

    async downloadWord(filename) {
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
                
                this.showMessage(`Downloaded Word document: ${filename}`, 'success');
            } else {
                throw new Error('Word download failed');
            }
        } catch (error) {
            console.error('Word download failed:', error);
            this.showMessage('Word download failed', 'error');
        }
    }

    async generateAndDownloadWord(jsonFilepath, product, pillar) {
        try {
            // Show progress bar
            this.showProgress();
            this.updateProgress(10, 'Loading analysis data...');
            
            // Create analysis data for Word generation
            const analysisData = {
                metadata: {
                    pillar: pillar,
                    product: product,
                    region: 'GLOBAL',
                    timestamp: new Date().toISOString()
                },
                analysis: {
                    pillar: pillar,
                    product: product,
                    region: 'GLOBAL',
                    questions_asked: [],
                    answers: [],
                    conversation_flow: [],
                    key_points: [],
                    timestamp: new Date().toISOString()
                }
            };
            
            // Load the actual JSON data
            this.updateProgress(30, 'Loading analysis data...');
            const response = await fetch(`${this.apiBase}/download/${jsonFilepath}`);
            if (response.ok) {
                const jsonData = await response.json();
                analysisData.analysis = jsonData;
            }
            
            // Generate Word document
            this.updateProgress(60, 'Generating Word document...');
            const wordResponse = await fetch(`${this.apiBase}/generate-word`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(analysisData)
            });
            
            const wordData = await wordResponse.json();
            
            if (wordData.success) {
                // Download the generated Word document
                this.updateProgress(90, 'Preparing download...');
                await this.downloadWord(wordData.filename);
                this.updateProgress(100, 'Word document ready!');
                this.hideProgress();
                this.showMessage('Word document generated and downloaded successfully!', 'success');
            } else {
                throw new Error(wordData.error || 'Word generation failed');
            }
            
        } catch (error) {
            console.error('Word generation failed:', error);
            this.hideProgress();
            this.showMessage(`Word generation failed: ${error.message}`, 'error');
        }
    }

    async generateAndDownloadCombinedWord(jsonFilepath, products, pillar) {
        try {
            // Show progress bar
            this.showProgress();
            this.updateProgress(10, 'Loading combined analysis data...');
            
            // Load the actual JSON data
            this.updateProgress(30, 'Loading combined analysis data...');
            const response = await fetch(`${this.apiBase}/download/${jsonFilepath}`);
            if (response.ok) {
                const combinedData = await response.json();
                
                // Generate combined Word document
                this.updateProgress(60, 'Generating combined Word document...');
                const wordResponse = await fetch(`${this.apiBase}/generate-combined-word`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(combinedData)
                });
                
                const wordData = await wordResponse.json();
                
                if (wordData.success) {
                    // Download the generated Word document
                    this.updateProgress(90, 'Preparing download...');
                    await this.downloadWord(wordData.filename);
                    this.updateProgress(100, 'Combined Word document ready!');
                    this.hideProgress();
                    this.showMessage('Combined Word document generated and downloaded successfully!', 'success');
                } else {
                    throw new Error(wordData.error || 'Combined Word generation failed');
                }
            } else {
                throw new Error('Failed to load combined analysis data');
            }
            
        } catch (error) {
            console.error('Combined Word generation failed:', error);
            this.hideProgress();
            this.showMessage(`Combined Word generation failed: ${error.message}`, 'error');
        }
    }

    async refreshData() {
        this.loadHistory();
        this.loadReports();
        this.testConnection();
        this.showMessage('Data refreshed', 'success');
    }

    async clearHistory() {
        if (!confirm('Are you sure you want to clear all history and generated files? This action cannot be undone.')) {
            return;
        }

        const btn = document.getElementById('clearHistoryBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<div class="loading"></div> Clearing...';
        btn.disabled = true;

        try {
            const response = await fetch(`${this.apiBase}/clear-history`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const data = await response.json();

            if (data.success) {
                this.showMessage(`Cleared ${data.count} files successfully`, 'success');
                this.loadHistory();
                this.loadReports();
            } else {
                throw new Error(data.error || 'Failed to clear history');
            }
        } catch (error) {
            console.error('Clear history failed:', error);
            this.showMessage(`Clear history failed: ${error.message}`, 'error');
        } finally {
            btn.innerHTML = originalText;
            btn.disabled = false;
        }
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
