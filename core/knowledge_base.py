"""
Knowledge Base Engine for 226 AI Paradigms, Obscure Architectures, and Mathematics.
Provides offline indexed semantic and lexical retrieval.
"""
import os
import json
import math
import re
from typing import List, Dict, Any, Optional

KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "ai_knowledge_226.json")

class AIKnowledgeEngine:
    def __init__(self, json_path: str = KNOWLEDGE_FILE):
        self.json_path = os.path.abspath(json_path)
        self.domains: List[Dict[str, Any]] = []
        self.vocab = {}
        self.doc_freq = {}
        self.load()

    def load(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f"Knowledge database not found at {self.json_path}")
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.domains = data.get("domains", [])
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r"[a-z0-9_\-\.\+]+", text)
        return tokens

    def _build_index(self):
        self.doc_freq = {}
        num_docs = len(self.domains)
        for doc in self.domains:
            content = f"{doc.get('name', '')} {doc.get('category', '')} {doc.get('concept', '')} {doc.get('mathematical_basis', '')} {doc.get('obscure_insights', '')}"
            tokens = set(self._tokenize(content))
            for t in tokens:
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1

    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        tokens = self._tokenize(query_text)
        if not tokens:
            return self.domains[:top_k]

        scores = []
        num_docs = len(self.domains)

        for doc in self.domains:
            score = 0.0
            name_tokens = self._tokenize(doc.get("name", ""))
            category_tokens = self._tokenize(doc.get("category", ""))
            concept_tokens = self._tokenize(doc.get("concept", ""))
            math_tokens = self._tokenize(doc.get("mathematical_basis", ""))
            obscure_tokens = self._tokenize(doc.get("obscure_insights", ""))

            for t in tokens:
                # IDF weight
                df = self.doc_freq.get(t, 1)
                idf = math.log((num_docs + 1) / (df + 1)) + 1.0

                # Priority matching
                tf = 0
                if t in name_tokens:
                    tf += 15.0
                if t in category_tokens:
                    tf += 6.0
                if t in concept_tokens:
                    tf += 3.0
                if t in math_tokens:
                    tf += 4.0
                if t in obscure_tokens:
                    tf += 5.0

                score += tf * idf

            scores.append((score, doc))

        # Sort descending by score
        scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scores[:top_k]]

    def get_by_id(self, topic_id: int) -> Optional[Dict[str, Any]]:
        for d in self.domains:
            if d.get("id") == topic_id:
                return d
        return None

    def get_category_summary(self) -> Dict[str, int]:
        summary = {}
        for d in self.domains:
            cat = d.get("category", "Uncategorized")
            summary[cat] = summary.get(cat, 0) + 1
        return summary

    def format_knowledge_context(self, user_query: str, max_records: int = 3) -> str:
        matches = self.query(user_query, top_k=max_records)
        if not matches:
            return ""
        
        ctx = "=== RETRIEVED HIGH-END AI DOMAIN KNOWLEDGE (226 EXPERT SUBFIELDS) ===\n"
        for m in matches:
            ctx += f"\n[Field #{m.get('id')}: {m.get('name')}] (Category: {m.get('category')})\n"
            ctx += f"  - Concept: {m.get('concept')}\n"
            ctx += f"  - Mathematical Formulation: {m.get('mathematical_basis')}\n"
            ctx += f"  - Obscure & Edge Insights: {m.get('obscure_insights')}\n"
            ctx += f"  - Frameworks & Implementations: {m.get('open_source_frameworks')}\n"
        ctx += "========================================================================\n"
        return ctx

# Self-test if run directly
if __name__ == "__main__":
    engine = AIKnowledgeEngine()
    print(f"Loaded {len(engine.domains)} AI domain records.")
    print("Categories:", engine.get_category_summary())
    test_q = "How do Kolmogorov-Arnold Networks differ from Liquid Neural Networks?"
    print("\nTest Search:", test_q)
    print(engine.format_knowledge_context(test_q, max_records=2))

