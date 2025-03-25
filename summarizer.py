from transformers import pipeline
from dotenv import load_dotenv
import os

load_dotenv()

class Summarizer:
    def __init__(self):
        try:
            self.brief_summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,
                framework="pt"
            )
            self.detailed_summarizer = pipeline(
                "summarization",
                model="philschmid/flan-t5-base-samsum",
                device=-1,
                framework="pt"
            )
        except Exception as e:
            print(f"Error initializing summarizers: {str(e)}")
            raise

    def _prepare_text(self, articles):
        return " ".join([f"{a['title']} {a['content']}" for a in articles])

    def summarize_brief(self, articles):
        try:
            text = self._prepare_text(articles)
            return self.brief_summarizer(text, max_length=100, min_length=30)[0]['summary_text']
        except Exception as e:
            print(f"Brief summarization error: {str(e)}")
            return "Could not generate brief summary"

    def summarize_detailed(self, articles):
        try:
            text = self._prepare_text(articles)
            return self.detailed_summarizer(text, max_length=300)[0]['summary_text']
        except Exception as e:
            print(f"Detailed summarization error: {str(e)}")
            return "Could not generate detailed summary"