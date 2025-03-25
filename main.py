import json
from news_retriever import NewsRetriever
from embedding_engine import EmbeddingEngine
from summarizer import Summarizer
from user_manager import UserManager
from dotenv import load_dotenv
import os

load_dotenv()

class NewsApp:
    def __init__(self):
        self.retriever = NewsRetriever()
        self.embedder = EmbeddingEngine()
        self.summarizer = Summarizer()
        self.user = UserManager()

    def run(self):
        print("\n=== News Summarizer ===")
        while True:
            print("\n1. Search news\n2. Saved topics\n3. History\n4. Exit")
            choice = input("Choose option (1-4): ").strip()
            
            if choice == "1":
                self._handle_search()
            elif choice == "2":
                self._show_saved_topics()
            elif choice == "3":
                self._show_history()
            elif choice == "4":
                print("\nGoodbye!")
                break
            else:
                print("Invalid option. Please try again.")

    def _handle_search(self):
        query = input("\nEnter search query: ").strip()
        if not query:
            print("Query cannot be empty")
            return
            
        print("\nSearching for news...")
        articles = self.retriever.fetch_articles(query)
        
        if not articles:
            print("No articles found for this query")
            return
            
        print(f"\nFound {len(articles)} articles:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']} ({article['source']})")
        
        if not self.embedder.create_embeddings(articles):
            print("Warning: Could not create embeddings for these articles")
        
        self.user.add_history(query, articles)
        
        while True:
            summary_type = input("\nChoose summary type (brief/detailed/back): ").lower()
            if summary_type == "back":
                break
            elif summary_type == "brief":
                print("\nBrief Summary:")
                print(self.summarizer.summarize_brief(articles))
            elif summary_type == "detailed":
                print("\nDetailed Summary:")
                print(self.summarizer.summarize_detailed(articles))
            else:
                print("Invalid choice")
        
        if input("\nSave this topic? (y/n): ").lower() == "y":
            if self.user.add_topic(query):
                print("Topic saved successfully")
            else:
                print("Topic already exists")

    def _show_saved_topics(self):
        topics = self.user.get_prefs()["topics"]
        if not topics:
            print("\nNo saved topics yet")
            return
            
        print("\nSaved Topics:")
        for i, topic in enumerate(topics, 1):
            print(f"{i}. {topic}")
        
        print("\nOptions:")
        print("1. Search a saved topic")
        print("2. Delete a topic")
        print("3. Back")
        
        choice = input("Choose option (1-3): ").strip()
        if choice == "1":
            topic_num = input("Enter topic number to search: ").strip()
            try:
                topic = topics[int(topic_num)-1]
                self._handle_search(topic)
            except (ValueError, IndexError):
                print("Invalid topic number")
        elif choice == "2":
            topic_num = input("Enter topic number to delete: ").strip()
            try:
                topic = topics[int(topic_num)-1]
                self._delete_topic(topic)
            except (ValueError, IndexError):
                print("Invalid topic number")

    def _delete_topic(self, topic):
        prefs = self.user.get_prefs()
        if topic in prefs["topics"]:
            prefs["topics"].remove(topic)
            self.user.save_prefs(prefs)
            print(f"Deleted topic: {topic}")
        else:
            print("Topic not found")

    def _show_history(self):
        history = self.user.get_history()
        if not history:
            print("\nNo search history yet")
            return
            
        print("\nSearch History (newest first):")
        for i, entry in enumerate(reversed(history), 1):
            print(f"\n{i}. {entry['query']} ({entry['timestamp']})")
            print("   Articles:")
            for article in entry["articles"][:3]:
                print(f"   - {article['title']} ({article['source']})")

if __name__ == "__main__":
    try:
        app = NewsApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted")
    except Exception as e:
        print(f"\nFatal error: {str(e)}")