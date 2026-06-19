import json
import hashlib
from datetime import datetime
from pathlib import Path

class AuditLogger:
    def __init__(self, log_dir: str = "./audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.log_file = self.log_dir / f"audit_{datetime.now().strftime('%Y%m%d')}.jsonl"
    
    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def log(self, query: str, decision: str, risk_level: str, answer: str):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "query_hash": self._hash(query),
            "router_decision": decision,
            "risk_level": risk_level,
            "answer_hash": self._hash(answer),
            "compliance": {
                "nist": "GOVERN 1.3",
                "eu_ai_act": "Article 12",
                "dpdp": "Section 12"
            }
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return entry["query_hash"]

if __name__ == "__main__":
    logger = AuditLogger()
    h = logger.log("test query", "retrieve", "low", "test answer")
    print(f"Logged: {h}")