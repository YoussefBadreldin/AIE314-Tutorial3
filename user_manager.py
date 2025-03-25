import json
import os
from datetime import datetime

class UserManager:
    def __init__(self, user_id="default"):
        self.user_id = user_id
        self.data_dir = "user_data"
        os.makedirs(self.data_dir, exist_ok=True)
        self.prefs_file = f"{self.data_dir}/user_{user_id}_prefs.json"
        self.history_file = f"{self.data_dir}/user_{user_id}_history.json"
        self._init_files()

    def _init_files(self):
        defaults = {
            "prefs": {"topics": [], "style": "brief"},
            "history": []
        }
        
        for file, default in zip([self.prefs_file, self.history_file], defaults.values()):
            if not os.path.exists(file):
                with open(file, "w") as f:
                    json.dump(default, f)

    def add_topic(self, topic):
        try:
            prefs = self.get_prefs()
            if topic not in prefs["topics"]:
                prefs["topics"].append(topic)
                self.save_prefs(prefs)
                return True
            return False
        except Exception as e:
            print(f"Error adding topic: {str(e)}")
            return False

    def get_prefs(self):
        try:
            with open(self.prefs_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading preferences: {str(e)}")
            return {"topics": [], "style": "brief"}

    def save_prefs(self, prefs):
        try:
            with open(self.prefs_file, "w") as f:
                json.dump(prefs, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {str(e)}")

    def add_history(self, query, articles):
        try:
            with open(self.history_file, "r") as f:
                history = json.load(f)
            
            history.append({
                "query": query,
                "articles": [{"title": a["title"], "source": a["source"]} for a in articles],
                "timestamp": datetime.now().isoformat()
            })
            
            with open(self.history_file, "w") as f:
                json.dump(history, f, indent=2)
        except Exception as e:
            print(f"Error adding history: {str(e)}")

    def get_history(self):
        try:
            with open(self.history_file, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {str(e)}")
            return []