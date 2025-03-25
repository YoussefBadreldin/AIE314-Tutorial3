from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
import os

class EmbeddingEngine:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = PersistentClient(path="chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="news_articles",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )

    def create_embeddings(self, articles):
        try:
            documents = []
            metadatas = []
            ids = []
            
            for i, article in enumerate(articles):
                text = f"{article['title']}\n{article['content']}"
                documents.append(text)
                metadatas.append({
                    "source": article["source"],
                    "url": article["url"],
                    "date": article["publishedAt"]
                })
                ids.append(str(i))
            
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return True
            
        except Exception as e:
            print(f"Error creating embeddings: {str(e)}")
            return False

    def find_similar(self, query, k=3):
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            return results
        except Exception as e:
            print(f"Error finding similar articles: {str(e)}")
            return None