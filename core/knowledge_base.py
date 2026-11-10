import os
import json
import math
import re
from typing import List, Dict, Any, Optional

KNOWLEDGE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'ai_knowledge_226.json')

class AIKnowledgeEngine:

    def __init__(self, json_path: str = KNOWLEDGE_FILE):
        self.json_path = os.path.abspath(json_path)
        self.domains: List[Dict[str, Any]] = []
        self.inverted_index: Dict[str, List[tuple]] = {}
        self.doc_freq: Dict[str, int] = {}
        self.categories: Dict[str, List[Dict[str, Any]]] = {}
        self.query_cache: Dict[str, List[Dict[str, Any]]] = {}
        self.load()

    def load(self):
        if not os.path.exists(self.json_path):
            raise FileNotFoundError(f'Knowledge database not found at {self.json_path}')
        with open(self.json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.domains = data.get('domains', [])
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        return re.findall('[a-z0-9_\\-\\.\\+]+', text.lower())

    def _build_index(self):
        self.inverted_index.clear()
        self.doc_freq.clear()
        self.categories.clear()
        self.query_cache.clear()

        for idx, doc in enumerate(self.domains):
            cat = doc.get('category', 'General')
            if cat not in self.categories:
                self.categories[cat] = []
            self.categories[cat].append(doc)

            weights = {}
            for t in self._tokenize(doc.get('name', '')):
                weights[t] = weights.get(t, 0.0) + 16.0
            for t in self._tokenize(doc.get('category', '')):
                weights[t] = weights.get(t, 0.0) + 7.0
            for t in self._tokenize(doc.get('concept', '')):
                weights[t] = weights.get(t, 0.0) + 3.5
            for t in self._tokenize(doc.get('mathematical_basis', '')):
                weights[t] = weights.get(t, 0.0) + 4.5
            for t in self._tokenize(doc.get('obscure_insights', '')):
                weights[t] = weights.get(t, 0.0) + 5.5
            for t in self._tokenize(doc.get('open_source_frameworks', '')):
                weights[t] = weights.get(t, 0.0) + 4.0

            for t, w in weights.items():
                self.doc_freq[t] = self.doc_freq.get(t, 0) + 1
                if t not in self.inverted_index:
                    self.inverted_index[t] = []
                self.inverted_index[t].append((idx, w))

    def query(self, query_text: str, top_k: int = 3) -> List[Dict[str, Any]]:
        clean_q = query_text.strip().lower()
        if not clean_q:
            return self.domains[:top_k]

        if clean_q in self.query_cache:
            return self.query_cache[clean_q][:top_k]

        tokens = self._tokenize(clean_q)
        if not tokens:
            return self.domains[:top_k]

        scores: Dict[int, float] = {}
        num_docs = len(self.domains)

        for t in tokens:
            if t in self.inverted_index:
                df = self.doc_freq.get(t, 1)
                idf = math.log((num_docs + 1) / (df + 1)) + 1.0
                for doc_idx, weight in self.inverted_index[t]:
                    scores[doc_idx] = scores.get(doc_idx, 0.0) + (weight * idf)

        if not scores:
            return self.domains[:top_k]

        ranked_indices = sorted(scores.keys(), key=lambda i: scores[i], reverse=True)
        results = [self.domains[i] for i in ranked_indices[:max(top_k, 5)]]
        self.query_cache[clean_q] = results
        return results[:top_k]

    def deep_research(self, topic_query: str) -> Dict[str, Any]:
        matches = self.query(topic_query, top_k=2)
        if not matches:
            return {
                "found": False,
                "summary": f"No direct paradigm match found in 226 offline databases for '{topic_query}'.",
                "markdown": f"### 🔬 Offline Research: {topic_query}\nNo direct paradigm match found."
            }

        primary = matches[0]
        secondary = matches[1] if len(matches) > 1 else None

        md = f"### 🔬 OFFLINE RESEARCH DOSSIER: #{primary.get('id')} {primary.get('name')}\n"
        md += f"**Category**: `{primary.get('category')}`\n\n"
        md += f"#### 💡 Core Algorithmic Concept\n{primary.get('concept')}\n\n"

        concept_text = primary.get('concept', '')
        if concept_text and len(concept_text) > 30:
            sentences = concept_text.replace('. ', '.\n').split('\n')
            if len(sentences) > 1:
                md += f"**In plain terms**: {sentences[0]}\n\n"
                for s in sentences[1:]:
                    if s.strip():
                        md += f"- {s.strip()}\n"
                md += "\n"

        md += f"#### 📐 Mathematical & Theoretical Formulation\n```text\n{primary.get('mathematical_basis')}\n```\n\n"

        math_basis = primary.get('mathematical_basis', '')
        if math_basis and len(math_basis) > 20:
            md += f"**What the math means**: This formulation captures "
            md += f"the essential computational structure of {primary.get('name')}. "
            md += f"It defines the precise relationships between inputs, transformations, and outputs that give this paradigm its power.\n\n"

        md += f"#### 🧬 Obscure Invariants & Latent Insights\n{primary.get('obscure_insights')}\n\n"

        insights = primary.get('obscure_insights', '')
        if insights and len(insights) > 20:
            md += f"**Why this matters**: These insights reveal edge cases and advanced properties "
            md += f"that practitioners must understand to avoid pitfalls and unlock peak performance.\n\n"

        md += f"#### 🛠️ Production Frameworks & Implementations\n`{primary.get('open_source_frameworks')}`\n\n"

        md += f"#### 🌍 Real-World Applications\n"
        md += f"{primary.get('name')} is actively used in production AI systems across domains including "
        md += f"large-scale model training, inference optimization, autonomous systems, and research. "
        md += f"Its {primary.get('category')} paradigm class makes it especially relevant to modern deep learning pipelines.\n"

        if secondary:
            md += f"\n---\n**🔗 Cross-Domain Correlated Paradigm**: #{secondary.get('id')} {secondary.get('name')} ({secondary.get('category')})\n"
            md += f"- *Core Concept*: {secondary.get('concept')}\n"
            md += f"- *Mathematical Link*: `{secondary.get('mathematical_basis')}`\n"
            md += f"- *Shared Edge Insight*: {secondary.get('obscure_insights')}\n"
            md += f"- *Frameworks*: `{secondary.get('open_source_frameworks')}`\n"

        short_summary = f"[{primary.get('name')}]: {primary.get('concept')} Math: {primary.get('mathematical_basis')}"

        return {
            "found": True,
            "primary": primary,
            "secondary": secondary,
            "short_summary": short_summary,
            "markdown": md
        }

    def compare_paradigms(self, topic_a: str, topic_b: str) -> str:
        matches_a = self.query(topic_a, top_k=1)
        matches_b = self.query(topic_b, top_k=1)

        if not matches_a or not matches_b:
            return f"Comparison unavailable: unable to resolve both '{topic_a}' and '{topic_b}' in 226 offline database."

        da = matches_a[0]
        db = matches_b[0]

        md = f"### ⚖️ ARCHITECTURAL COMPARISON: {da.get('name')} vs {db.get('name')}\n\n"
        md += f"| Dimension | #{da.get('id')} {da.get('name')} | #{db.get('id')} {db.get('name')} |\n"
        md += "| :--- | :--- | :--- |\n"
        md += f"| **Category** | {da.get('category')} | {db.get('category')} |\n"
        md += f"| **Core Concept** | {da.get('concept')} | {db.get('concept')} |\n"
        md += f"| **Mathematical Formulation** | `{da.get('mathematical_basis')}` | `{db.get('mathematical_basis')}` |\n"
        md += f"| **Obscure Edge Insight** | {da.get('obscure_insights')} | {db.get('obscure_insights')} |\n"
        md += f"| **Framework Stack** | {da.get('open_source_frameworks')} | {db.get('open_source_frameworks')} |\n"

        return md

    def get_by_id(self, topic_id: int) -> Optional[Dict[str, Any]]:
        for d in self.domains:
            if d.get('id') == topic_id:
                return d
        return None

    def get_all_categories(self) -> List[str]:
        return list(self.categories.keys())

    def get_category_domains(self, category: str) -> List[Dict[str, Any]]:
        return self.categories.get(category, [])

    def get_category_summary(self) -> Dict[str, int]:
        return {cat: len(docs) for cat, docs in self.categories.items()}

    def format_knowledge_context(self, user_query: str, max_records: int = 3) -> str:
        matches = self.query(user_query, top_k=max_records)
        if not matches:
            return ''
        ctx = '=== RETRIEVED HIGH-END AI DOMAIN KNOWLEDGE (226 EXPERT SUBFIELDS) ===\n'
        for m in matches:
            ctx += f"\n[Field #{m.get('id')}: {m.get('name')}] (Category: {m.get('category')})\n"
            ctx += f"  - Concept: {m.get('concept')}\n"
            ctx += f"  - Mathematical Formulation: {m.get('mathematical_basis')}\n"
            ctx += f"  - Obscure & Edge Insights: {m.get('obscure_insights')}\n"
            ctx += f"  - Frameworks & Implementations: {m.get('open_source_frameworks')}\n"
        ctx += '========================================================================\n'
        return ctx

if __name__ == '__main__':
    engine = AIKnowledgeEngine()
    print(f'Loaded {len(engine.domains)} AI domain records.')
    print('Categories:', engine.get_category_summary())
    res = engine.deep_research('Mamba')
    print(res['markdown'])
