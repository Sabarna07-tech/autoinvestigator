import os
from pathlib import Path

root_dir = "./"

files = [
    "server/__init__.py",
    "server/tools/__init__.py",
    "server/tools/web_search.py",
    "server/tools/pdf_reader.py",
    "server/tools/news_aggregator.py",
    "server/tools/news_scanner.py",
    "server/tools/financial_data.py",
    "server/tools/sec_filings.py",
    "server/tools/ticker_manager.py",
    
    "server/resources/__init__.py",
    "server/resources/memory_store.py",
    "server/resources/knowledge_base/red_flags.json",
    "server/resources/knowledge_base/risk_rules.md",
    
    "server/prompts/__init__.py",
    "server/prompts/company_profile.txt",
    "server/prompts/news_summary.txt",
    "server/prompts/risk_assessment.txt",
    "server/prompts/financial_analysis.txt",
    "server/main.py",
    
    "client/__init__.py",
    "client/agents/__init__.py",
    "client/agents/company_profiler.py",
    "client/agents/news_watcher.py",
    "client/agents/sentiment_tracker.py",
    "client/agents/risk_reporter.py",
    "client/agents/user_advisor.py",
    "client/agents/financial_intel.py",
    "client/agents/risk_radar.py",
    
    "client/orchestrator.py",
    "client/ui.py",
    "client/demo.py",
    "client/mcp_client.py",

    "shared/__init__.py",
    "shared/utils.py",
    "shared/config.py",
    "shared/gemini.py",
    
    ".env",
    ".gitignore",
    "requirements.txt",
    "README.md"
]


for file_path in files:
        full_path = os.path.join(root_dir, file_path)
        directory = os.path.dirname(full_path)
        
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
            
        if not os.path.exists(full_path):
            with open(full_path, 'w') as f:
                pass
            print(f"Created file: {full_path}")
        else:
            print(f"File already exists: {full_path}")
