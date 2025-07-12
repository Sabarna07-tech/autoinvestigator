# server/tools/sentiment_analyzer.py

from transformers import pipeline

class SentimentAnalyzerTool:
    def __init__(self):
        # Using a distilled version for lighter compute requirements
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

    def run(self, text: str) -> dict:
        print(f"[SentimentAnalyzerTool] Analyzing sentiment for text.")
        # The pipeline returns a list of dictionaries
        results = self.sentiment_pipeline(text[:512]) # Truncate to model's max length
        print(results)
        return results[0] if results else {"label": "NEUTRAL", "score": 0.0}

if __name__=='__main__':
	ob = SentimentAnalyzerTool()
	print(ob.run("I am winning the match"))