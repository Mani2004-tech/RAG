import json
from datetime import datetime

class QueryTrace:

    def __init__(self, query):
        self.trace = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }

    def add_step(self, node_name, output=None):
        self.trace["steps"].append({
            "node": node_name,
            "output": str(output)[:1000] if output else None
        })

    def save(self):
        with open("query_trace.json", "w") as f:
            json.dump(self.trace, f, indent=2)