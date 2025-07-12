# AutoInvestigator: Multi-Agent AI System for Corporate Risk Intelligence

AutoInvestigator is an agentic AI system built using the MCP Server + MCP Client architecture. It automates corporate risk analysis by coordinating agents that perform web research, financial analysis, sentiment tracking, and risk reporting.

## 🚀 Quick Start with Gradio UI

The easiest way to use AutoInvestigator is through the interactive web interface:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Set up API key**: Copy `.env.example` to `.env` and add your `GEMINI_API_KEY`
3. **Start server**: `python server.py`
4. **Launch UI**: `python gradio_ui.py`
5. **Open browser**: Navigate to `http://localhost:7860`

See [GRADIO_UI_GUIDE.md](GRADIO_UI_GUIDE.md) for detailed documentation.

## Modules
- **MCP Server**: Hosts tools (web search, PDF reader, sentiment analyzer), resources (memory, knowledge base), and prompt templates.
- **MCP Client**: Coordinates multi-agent workflows that accomplish tasks like risk profiling, news analysis, and financial insight.
- **Gradio UI**: Interactive web interface for easy access to all functionalities.
- **Shared**: Utilities and configurations.
- **Data**: Stores cache and generated reports.