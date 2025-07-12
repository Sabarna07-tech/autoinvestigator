# AutoInvestigator Gradio UI

## Overview

The AutoInvestigator Gradio UI provides an interactive web interface for the AutoInvestigator multi-agent AI system. This interface allows users to easily access all the corporate risk intelligence functionalities through a user-friendly web application.

## Features

### 🎯 Core Functionality
- **Company Analysis**: Comprehensive risk analysis for any company
- **Multiple Analysis Types**: 
  - Full Analysis (complete risk assessment)
  - Company Profile (basic company information)
  - Financial Analysis (financial data and reports)
  - News & Risk Analysis (recent news and risk factors)
- **Email Reports**: Send analysis results via email
- **Real-time Status**: Live progress updates during analysis

### 🛠️ Available Tools Integration
- **Web Search**: Company profile research from multiple sources
- **Financial Data**: Real-time financial information and SEC filings
- **News Scanner**: Recent news analysis for risks and legal issues
- **Email Notifications**: Automated report delivery

## Setup and Installation

### Prerequisites
1. Python 3.8+
2. All dependencies from `requirements.txt`
3. Gemini API key (required for LLM functionality)

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Environment Variables**:
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your API key
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

3. **Start the Server**:
   ```bash
   python server.py
   ```

4. **Launch the UI**:
   ```bash
   python gradio_ui.py
   ```

5. **Access the Interface**:
   Open your browser to `http://localhost:7860`

## Usage Guide

### Basic Analysis
1. Enter a company name in the "Company Name or Query" field
2. Select the type of analysis from the dropdown
3. (Optional) Enter an email address to receive results
4. Click "🔍 Start Analysis"
5. View results in the tabbed interface below

### Analysis Types
- **Full Analysis**: Complete risk assessment including web research, financial data, and news analysis
- **Company Profile**: Basic company information and background
- **Financial Only**: Detailed financial analysis and SEC filings
- **News & Risk Only**: Recent news scanning for legal issues and risks

### Example Queries
- `Apple Inc` with "Full Analysis"
- `Tesla lawsuit risks` with "News & Risk Only"
- `Microsoft Corporation` with "Financial Only"
- `Amazon.com Inc` with "Company Profile"

## API Configuration

### Required Environment Variables
```bash
# Gemini API Key (Required)
GEMINI_API_KEY=your_gemini_api_key_here

# Server URL (Optional, defaults to local)
SERVER_URL=http://127.0.0.1:5000/requests

# Email Configuration (Optional)
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

### Getting API Keys
1. **Gemini API Key**: Get from [Google AI Studio](https://ai.google.dev/)
2. **Email Configuration**: Use Gmail app passwords for SMTP

## Architecture

### Components
- **gradio_ui.py**: Main Gradio interface
- **client/agent.py**: Core analysis agent
- **server.py**: Backend API server
- **server/tools/**: Individual tool implementations

### Data Flow
1. User inputs company query through Gradio UI
2. UI calls AutoInvestigatorAgent
3. Agent generates tool invocation plan using LLM
4. Agent executes tools via server API
5. Results processed and displayed in UI tabs

## Troubleshooting

### Common Issues

**API Key Error**:
```
❌ Error: Agent not initialized
Details: GEMINI_API_KEY is not set
```
- Solution: Set `GEMINI_API_KEY` in your `.env` file

**Server Connection Error**:
```
❌ Cannot connect to server
```
- Solution: Start the server with `python server.py`

**Email Sending Failed**:
```
⚠️ Email sending failed
```
- Solution: Configure email credentials in `.env` file

### Debug Mode
Run with debug logging:
```bash
export GRADIO_DEBUG=1
python gradio_ui.py
```

## Development

### File Structure
```
gradio_ui.py          # Main UI application
test_ui.py           # UI functionality tests
test_server.py       # Server connectivity tests
.env.example         # Environment variables template
client/
  ├── agent.py       # Core analysis agent
  ├── config.py      # Configuration management
  └── ...
server/
  ├── server.py      # Flask API server
  ├── interface.py   # Tool interface
  └── tools/         # Individual tools
```

### Extending the UI
To add new functionality:
1. Add new tools to `server/tools/`
2. Update `server/tool_descriptor.py`
3. Modify `gradio_ui.py` to include new UI elements
4. Test with `test_ui.py`

## Security Notes

- Keep API keys secure and never commit them to version control
- Use environment variables for sensitive configuration
- Consider using HTTPS in production deployments
- Regularly update dependencies

## License

Part of the AutoInvestigator project - see main README for license information.