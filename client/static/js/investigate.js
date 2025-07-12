// Investigation Interface JavaScript
class InvestigationInterface {
    constructor() {
        this.chatMessages = document.getElementById('chatMessages');
        this.userInput = document.getElementById('userInput');
        this.sendButton = document.getElementById('sendButton');
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.resultsContent = document.getElementById('resultsContent');
        this.clearResultsButton = document.getElementById('clearResults');
        this.toolItems = document.querySelectorAll('.tool-item');
        
        this.isLoading = false;
        this.selectedTool = 'all';
        
        this.initializeEventListeners();
        this.initializeAutoResize();
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
        
        // Tool selection
        this.toolItems.forEach(item => {
            item.addEventListener('click', () => this.selectTool(item));
        });
        
        // Clear results
        this.clearResultsButton.addEventListener('click', () => this.clearResults());
        
        // Focus input on load
        this.userInput.focus();
    }

    initializeAutoResize() {
        this.autoResize();
    }

    autoResize() {
        this.userInput.style.height = 'auto';
        this.userInput.style.height = Math.min(this.userInput.scrollHeight, 120) + 'px';
    }

    updateCharacterCount() {
        const count = this.userInput.value.length;
        const charCount = document.querySelector('.char-count');
        charCount.textContent = `${count}/1000`;
        
        // Change color when approaching limit
        if (count > 900) {
            charCount.style.color = '#ff6b6b';
        } else if (count > 800) {
            charCount.style.color = '#ffd93d';
        } else {
            charCount.style.color = '#808080';
        }
    }

    updateSendButtonState() {
        const hasText = this.userInput.value.trim().length > 0;
        this.sendButton.disabled = !hasText || this.isLoading;
    }

    selectTool(item) {
        // Remove active class from all tools
        this.toolItems.forEach(tool => tool.classList.remove('active'));
        
        // Add active class to selected tool
        item.classList.add('active');
        
        // Update selected tool
        this.selectedTool = item.dataset.tool;
        
        // Add visual feedback
        item.style.transform = 'scale(0.95)';
        setTimeout(() => {
            item.style.transform = 'scale(1)';
        }, 150);
    }

    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isLoading) return;

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

    addMessage(text, sender) {
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
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        content.appendChild(messageText);
        content.appendChild(messageTime);
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
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

    showLoading() {
        this.isLoading = true;
        this.loadingOverlay.classList.add('active');
        this.updateSendButtonState();
        
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
            steps.forEach((step, index) => {
                step.classList.remove('active');
            });
            
            if (currentStep < steps.length) {
                steps[currentStep].classList.add('active');
                currentStep++;
            } else {
                clearInterval(interval);
            }
        }, 1000);
    }

    updateResults(response) {
        if (!response.results) return;
        
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
                <h4>Investigation Results</h4>
                <span class="result-time">${timestamp}</span>
            </div>
            <div class="result-content">
                ${this.formatResults(response.results)}
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