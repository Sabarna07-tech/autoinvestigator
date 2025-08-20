// Investigation Interface JavaScript
class InvestigationInterface {
    constructor() {
        this.selectedTool = 'all';
        this.selectedFile = null;
        this.availableTools = {
            'all': {
                name: 'All Tools (Deep Research)',
                description: 'Uses all available analysis tools for comprehensive investigation',
                icon: 'fas fa-search-plus'
            },
            'financial': {
                name: 'Financial Data Analysis',
                description: 'Analyzes financial statements, ratios, and market data',
                icon: 'fas fa-chart-line'
            },
            'news': {
                name: 'News Analysis',
                description: 'Scans and analyzes recent news and market sentiment',
                icon: 'fas fa-newspaper'
            },
            'websearch': {
                name: 'Web Search',
                description: 'Searches the web for relevant information and data',
                icon: 'fas fa-globe'
            },
            'sec': {
                name: 'SEC Filings',
                description: 'Analyzes SEC filings and regulatory documents',
                icon: 'fas fa-file-alt'
            },
            'sentiment': {
                name: 'Sentiment Analysis',
                description: 'Analyzes market sentiment and social media trends',
                icon: 'fas fa-heart'
            },
            'risk': {
                name: 'Risk Assessment',
                description: 'Evaluates investment risks and potential concerns',
                icon: 'fas fa-shield-alt'
            },
            'gemini': {
                name: 'AI Analysis (Gemini)',
                description: 'Advanced AI-powered analysis and insights',
                icon: 'fas fa-brain'
            }
        };
        
        this.isLoading = false;
        this.initializeElements();
        this.initializeEventListeners();
        this.initializeAutoResize();
        this.loadChatHistory();
    }

    initializeElements() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.resultsContent = document.getElementById('resultsContent');
        this.clearResultsButton = document.getElementById('clearResults');
        this.toolItems = document.querySelectorAll('.sidebar .tool-item');
        
        // Tools dropdown elements
        this.toolsBtn = document.getElementById('toolsBtn');
        this.toolsDropdown = document.getElementById('toolsDropdown');
        this.dropdownToolItems = document.querySelectorAll('.tools-dropdown-menu .tool-item[data-tool]');
        
        // File upload elements
        this.fileInput = document.getElementById('fileInput');
        this.fileUploadBtn = document.getElementById('fileUploadBtn');
        this.fileIndicator = document.getElementById('fileIndicator');
        this.removeFileBtn = document.getElementById('removeFileBtn');
        
        // Character count
        this.charCount = document.getElementById('charCount');
    }

    initializeEventListeners() {
        // Send button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Enter key press
        this.userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Input change for character count and button state
        this.userInput.addEventListener('input', () => {
            this.updateCharacterCount();
            this.updateSendButtonState();
            this.autoResize();
        });
        
        // Sidebar tool selection
        this.toolItems.forEach(item => {
            item.addEventListener('click', () => this.selectToolFromSidebar(item));
        });
        
        // Tools dropdown toggle
        this.toolsBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleToolsDropdown();
        });

        // Dropdown tool selection
        this.dropdownToolItems.forEach(button => {
            button.addEventListener('click', (e) => {
                const tool = e.target.closest('.tool-item').dataset.tool;
                this.selectTool(tool);
                this.hideToolsDropdown();
            });
        });

        // File upload
        this.fileUploadBtn.addEventListener('click', () => {
            this.fileInput.click();
            this.hideToolsDropdown();
        });

        this.fileInput.addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files[0]);
        });

        // Remove file button
        if (this.removeFileBtn) {
            this.removeFileBtn.addEventListener('click', () => {
                this.removeFile();
            });
        }

        // Hide dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.toolsBtn.contains(e.target) && !this.toolsDropdown.contains(e.target)) {
                this.hideToolsDropdown();
            }
        });
        
        // Clear results
        this.clearResultsButton.addEventListener('click', () => this.clearResults());
        
        // Focus input on load
        this.userInput.focus();
    }

    initializeAutoResize() {
        this.autoResize();
    }

    async loadChatHistory() {
        try {

            const resp = await fetch('/api/history');
            if (!resp.ok) return;
            const data = await resp.json();
            let lastResults = null;
            data.forEach(msg => {
                this.addMessage(msg.content, msg.role, msg.timestamp);
                if (msg.role === 'ai') {
                    lastResults = msg.results;
                }
            });
            if (lastResults) {
                this.resultsContent.innerHTML = '';
                this.updateResults({ results: lastResults });
            }
        } catch (err) {
            console.error('Failed to load history:', err);

        }
    }

    autoResize() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }

    updateCharacterCount() {
        const count = this.userInput.value.length;
        if (this.charCount) {
            this.charCount.textContent = `${count}/1000`;
            
            // Change color when approaching limit
            if (count > 900) {
                this.charCount.style.color = '#ff6b6b';
            } else if (count > 800) {
                this.charCount.style.color = '#ffd93d';
            } else {
                this.charCount.style.color = '#808080';
            }
        }
    }

    updateSendButtonState() {
        const hasText = this.userInput.value.trim().length > 0;
        const hasFile = this.selectedFile !== null;
        this.sendButton.disabled = (!hasText && !hasFile) || this.isLoading;
    }

    // Tools Dropdown Methods
    toggleToolsDropdown() {
        this.toolsDropdown.classList.toggle('show');
        
        // Update button appearance when dropdown is open
        if (this.toolsDropdown.classList.contains('show')) {
            this.toolsBtn.style.background = 'rgba(102, 126, 234, 0.2)';
            this.toolsBtn.style.borderColor = 'rgba(102, 126, 234, 0.4)';
        } else {
            this.toolsBtn.style.background = 'rgba(255, 255, 255, 0.1)';
            this.toolsBtn.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    }

    hideToolsDropdown() {
        this.toolsDropdown.classList.remove('show');
        this.toolsBtn.style.background = 'rgba(255, 255, 255, 0.1)';
        this.toolsBtn.style.borderColor = 'rgba(255, 255, 255, 0.2)';
    }

    selectTool(tool) {
        this.selectedTool = tool;
        
        // Update visual selection in dropdown
        this.dropdownToolItems.forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const selectedBtn = document.querySelector(`.tools-dropdown-menu [data-tool="${tool}"]`);
        if (selectedBtn) {
            selectedBtn.classList.add('selected');
        }
        
        // Update tools button display
        this.updateToolsButtonDisplay(tool);
        
        // Update sidebar selection to match
        this.updateSidebarSelection(tool);
        
        console.log('Selected tool:', tool, this.availableTools[tool]);
        
        // Show tool selection feedback
        this.showToolSelectionFeedback(tool);
    }

    selectToolFromSidebar(item) {
        // Remove active class from all sidebar tools
        this.toolItems.forEach(tool => tool.classList.remove('active'));
        
        // Add active class to selected tool
        item.classList.add('active');
        
        // Update selected tool
        const tool = item.dataset.tool;
        if (tool) {
            this.selectedTool = tool;
            this.updateToolsButtonDisplay(tool);
            this.updateDropdownSelection(tool);
            this.showToolSelectionFeedback(tool);
        }
        
        // Add visual feedback
        item.style.transform = 'scale(0.95)';
        setTimeout(() => {
            item.style.transform = 'scale(1)';
        }, 150);
    }

    updateToolsButtonDisplay(tool) {
        const toolInfo = this.availableTools[tool];
        if (toolInfo) {
            const buttonText = this.toolsBtn.querySelector('span');
            buttonText.textContent = toolInfo.name.length > 20 ? 
                toolInfo.name.substring(0, 17) + '...' : toolInfo.name;
            
            // Update the tools icon
            const toolsIcon = this.toolsBtn.querySelector('.tools-icon');
            if (toolsIcon) {
                toolsIcon.className = toolInfo.icon + ' tools-icon';
            }
        }
    }

    updateSidebarSelection(tool) {
        // Update sidebar to match selected tool
        this.toolItems.forEach(item => {
            item.classList.remove('active');
        });
        
        const sidebarItem = document.querySelector(`.sidebar .tool-item[data-tool="${tool}"]`);
        if (sidebarItem) {
            sidebarItem.classList.add('active');
        }
    }

    updateDropdownSelection(tool) {
        // Update dropdown to match sidebar selection
        this.dropdownToolItems.forEach(btn => {
            btn.classList.remove('selected');
        });
        
        const dropdownItem = document.querySelector(`.tools-dropdown-menu [data-tool="${tool}"]`);
        if (dropdownItem) {
            dropdownItem.classList.add('selected');
        }
    }

    showToolSelectionFeedback(tool) {
        const toolInfo = this.availableTools[tool];
        if (toolInfo) {
            // Create notification
            const notification = document.createElement('div');
            notification.className = 'notification-item notification-slide-in';
            notification.innerHTML = `
                <div class="notification-content">
                    <i class="${toolInfo.icon}"></i>
                    <span><strong>${toolInfo.name}</strong> selected</span>
                </div>
            `;
            
            // Add to notification container
            let notificationContainer = document.getElementById('toolNotification');
            if (!notificationContainer) {
                notificationContainer = document.createElement('div');
                notificationContainer.id = 'toolNotification';
                notificationContainer.className = 'tool-notification';
                document.body.appendChild(notificationContainer);
            }
            
            notificationContainer.appendChild(notification);
            
            // Remove notification after 2 seconds
            setTimeout(() => {
                notification.className = 'notification-item notification-slide-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 2000);
        }
    }

    // File Upload Methods
    handleFileSelection(file) {
        if (!file) return;
        
        if (file.type !== 'application/pdf') {
            this.showError('Please select a PDF file.');
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) { // 50MB limit
            this.showError('File size too large. Maximum 50MB allowed.');
            return;
        }
        
        this.selectedFile = file;
        this.showFileIndicator(file);
        console.log('File selected:', file.name, 'Size:', this.formatFileSize(file.size));
    }

    showFileIndicator(file) {
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        
        if (fileName && fileSize) {
            fileName.textContent = file.name;
            fileSize.textContent = this.formatFileSize(file.size);
            this.fileIndicator.style.display = 'flex';
        }
        
        this.updateSendButtonState();
    }

    removeFile() {
        this.selectedFile = null;
        this.fileInput.value = '';
        this.fileIndicator.style.display = 'none';
        this.updateSendButtonState();
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        
        if (!message && !this.selectedFile) return;
        if (this.isLoading) return;

        // Handle file upload
        if (this.selectedFile) {
            await this.handleFileUpload();
            return;
        }

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.userInput.value = '';
        this.updateCharacterCount();
        this.updateSendButtonState();
        this.autoResize();
        
        // Show loading state
        this.showLoading();
        
        try {
            // Send to backend
            const response = await this.investigate(message);
            
            // Hide loading
            this.hideLoading();
            
            // Add AI response
            this.addMessage(response.message || 'Investigation completed successfully!', 'ai');
            
            // Update results panel
            this.updateResults(response);
            
        } catch (error) {
            console.error('Investigation error:', error);
            this.hideLoading();
            this.addMessage('Sorry, there was an error processing your request. Please try again.', 'ai');
        }
    }

    async handleFileUpload() {
        if (!this.selectedFile) return;

        // Add file upload message to chat
        this.addMessage(`Uploading and analyzing: ${this.selectedFile.name}`, 'user');
        
        // Show loading with PDF step
        this.showLoading(true);
        
        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);
            formData.append('tool', this.selectedTool);

            const response = await fetch('/api/upload-pdf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Hide loading
            this.hideLoading();
            
            // Add AI response with PDF analysis
            this.addMessage(this.formatPDFAnalysis(result), 'ai');
            
            // Update results panel
            this.updateResults(result);
            
            // Clean up
            this.removeFile();
            
        } catch (error) {
            console.error('File upload error:', error);
            this.hideLoading();
            this.addMessage('Sorry, there was an error processing your PDF file. Please try again.', 'ai');
        }
    }

    formatPDFAnalysis(result) {
        if (result.analysis) {
            return `
                <div class="pdf-analysis-result">
                    <h3>📄 PDF Analysis Complete</h3>
                    <div class="analysis-summary">
                        <p><strong>Document:</strong> ${result.filename || 'PDF Document'}</p>
                        <p><strong>Pages:</strong> ${result.pages || 'N/A'}</p>
                    </div>
                    <div class="analysis-content">
                        <h4>Analysis Results:</h4>
                        ${typeof result.analysis === 'string' ? 
                            `<p>${result.analysis}</p>` : 
                            this.formatStructuredMessage(result.analysis)
                        }
                    </div>
                </div>
            `;
        }
        return result.message || 'PDF analysis completed successfully!';
    }

    async investigate(query) {
        const response = await fetch('/api/investigate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                tool: this.selectedTool
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(text, sender, ts = null) {

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        
        const icon = document.createElement('i');
        icon.className = sender === 'user' ? 'fas fa-user' : 'fas fa-robot';
        avatar.appendChild(icon);
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const messageText = document.createElement('div');
        messageText.className = 'message-text';
        
        // Handle different content types
        if (typeof text === 'string') {
            messageText.innerHTML = this.formatMessage(text);
        } else {
            messageText.innerHTML = this.formatStructuredMessage(text);
        }
        
        const messageTime = document.createElement('div');

        messageTime.textContent = ts ? this.formatTimestamp(ts) : this.getCurrentTime();

        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    formatTimestamp(ts) {
        const date = new Date(ts * 1000);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    formatMessage(text) {
        // Convert URLs to links
        text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" style="color: #667eea;">$1</a>');
        
        // Convert line breaks to paragraphs
        return text.split('\n').map(line => `<p>${line}</p>`).join('');
    }

    formatStructuredMessage(data) {
        let html = '';
        
        if (data.title) {
            html += `<h4 style="margin-bottom: 0.5rem; color: #667eea;">${data.title}</h4>`;
        }
        
        if (data.summary) {
            html += `<p><strong>Summary:</strong> ${data.summary}</p>`;
        }
        
        if (data.keyPoints && data.keyPoints.length > 0) {
            html += '<p><strong>Key Points:</strong></p><ul>';
            data.keyPoints.forEach(point => {
                html += `<li>${point}</li>`;
            });
            html += '</ul>';
        }
        
        if (data.recommendations && data.recommendations.length > 0) {
            html += '<p><strong>Recommendations:</strong></p><ul>';
            data.recommendations.forEach(rec => {
                html += `<li>${rec}</li>`;
            });
            html += '</ul>';
        }
        
        return html;
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showLoading(isPDF = false) {
        this.isLoading = true;
        this.loadingOverlay.classList.add('active');
        this.updateSendButtonState();
        
        // Show PDF step if needed
        const pdfStep = document.getElementById('step4');
        if (pdfStep) {
            pdfStep.style.display = isPDF ? 'flex' : 'none';
        }
        
        // Animate loading steps
        this.animateLoadingSteps();
    }

    hideLoading() {
        this.isLoading = false;
        this.loadingOverlay.classList.remove('active');
        this.updateSendButtonState();
    }

    animateLoadingSteps() {
        const steps = document.querySelectorAll('.loading-steps .step');
        let currentStep = 0;
        
        const interval = setInterval(() => {
            if (!this.isLoading) {
                clearInterval(interval);
                return;
            }
            
            steps.forEach((step, index) => {
                step.classList.remove('active');
            });
            
            if (currentStep < steps.length) {
                if (steps[currentStep].style.display !== 'none') {
                    steps[currentStep].classList.add('active');
                }
                currentStep++;
            } else {
                currentStep = 0; // Loop back to start
            }
        }, 1000);
    }

    updateResults(response) {
        if (!response.results && !response.analysis) return;
        
        // Clear empty state
        const emptyState = this.resultsContent.querySelector('.empty-state');
        if (emptyState) {
            emptyState.remove();
        }
        
        // Create results container
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'investigation-result';
        
        const timestamp = new Date().toLocaleString();
        resultsContainer.innerHTML = `
            <div class="result-header">
                <h4>${response.analysis ? 'PDF Analysis Results' : 'Investigation Results'}</h4>
                <span class="result-time">${timestamp}</span>
            </div>
            <div class="result-content">
                ${this.formatResults(response.results || response.analysis)}
            </div>
        `;
        
        this.resultsContent.appendChild(resultsContainer);
        this.resultsContent.scrollTop = this.resultsContent.scrollHeight;
    }

    formatResults(results) {
        let html = '';
        
        if (typeof results === 'string') {
            html = `<p>${results}</p>`;
        } else if (typeof results === 'object') {
            if (results.financial) {
                html += '<div class="result-section"><h5>Financial Data</h5><p>' + results.financial + '</p></div>';
            }
            if (results.news) {
                html += '<div class="result-section"><h5>News Analysis</h5><p>' + results.news + '</p></div>';
            }
            if (results.sentiment) {
                html += '<div class="result-section"><h5>Sentiment Analysis</h5><p>' + results.sentiment + '</p></div>';
            }
            if (results.risk) {
                html += '<div class="result-section"><h5>Risk Assessment</h5><p>' + results.risk + '</p></div>';
            }
        }
        
        return html || '<p>Results will appear here after investigation.</p>';
    }

    clearResults() {
        this.resultsContent.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <p>Start an investigation to see results here</p>
            </div>
        `;
    }

    showError(message) {
        console.error(message);
        this.addMessage(`❌ Error: ${message}`, 'ai');
    }
}

// Initialize the interface when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const interface = new InvestigationInterface();
    
    // Add some CSS for results styling
    const style = document.createElement('style');
    style.textContent = `
        .investigation-result {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            animation: slideInUp 0.3s ease;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .result-header h4 {
            color: white;
            font-size: 1rem;
            font-weight: 600;
        }
        
        .result-time {
            font-size: 0.8rem;
            color: #808080;
        }
        
        .result-section {
            margin-bottom: 1rem;
        }
        
        .result-section h5 {
            color: #667eea;
            font-size: 0.9rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .result-section p {
            color: #d0d0d0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        .result-content {
            color: #d0d0d0;
            font-size: 0.9rem;
            line-height: 1.5;
        }
    `;
    document.head.appendChild(style);
});
