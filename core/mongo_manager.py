import os
import sys
import json
import time
import hashlib
from typing import Dict, Any, List, Optional

try:
    import pymongo
    from pymongo import MongoClient
    PYMONGO_AVAILABLE = True
except ImportError:
    PYMONGO_AVAILABLE = False

class MongoDBManager:

    def __init__(self, uri: Optional[str] = None, db_name: str = "offline_ai_nexus"):
        self.uri = uri or os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = db_name
        self.client = None
        self.db = None
        self.is_connected = False
        self._init_connection()

    def _init_connection(self):
        if not PYMONGO_AVAILABLE:
            return
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self.is_connected = True
        except Exception:
            self.is_connected = False
            self.client = None
            self.db = None

    def connect(self, uri: str) -> Dict[str, Any]:
        self.uri = uri
        self._init_connection()
        return {
            "success": self.is_connected,
            "uri": self.uri,
            "db_name": self.db_name,
            "message": "Connected to MongoDB." if self.is_connected else "Could not connect to MongoDB server."
        }

    def sync_knowledge_base(self, json_path: str) -> Dict[str, Any]:
        if not os.path.exists(json_path):
            return {"success": False, "error": f"File not found: {json_path}"}
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            domains = data.get("domains", [])
            if self.is_connected and self.db is not None:
                col = self.db["ai_knowledge_226"]
                col.delete_many({})
                if domains:
                    col.insert_many(domains)
                return {"success": True, "count": len(domains), "collection": "ai_knowledge_226"}
            else:
                out_dir = os.path.join(os.path.dirname(json_path), "mongodb_export")
                os.makedirs(out_dir, exist_ok=True)
                export_path = os.path.join(out_dir, "ai_knowledge_226.json")
                with open(export_path, "w", encoding="utf-8") as ef:
                    json.dump(domains, ef, indent=2)
                return {"success": True, "count": len(domains), "collection": "ai_knowledge_226", "exported_to": export_path, "note": "Offline JSON backup saved"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def sync_blockchain_ledger(self, ledger_path: str) -> Dict[str, Any]:
        if not os.path.exists(ledger_path):
            return {"success": False, "error": f"File not found: {ledger_path}"}
        try:
            with open(ledger_path, "r", encoding="utf-8") as f:
                ledger = json.load(f)
            if self.is_connected and self.db is not None:
                col = self.db["blockchain_ledger"]
                col.delete_many({})
                if ledger:
                    col.insert_many(ledger)
                return {"success": True, "count": len(ledger), "collection": "blockchain_ledger"}
            else:
                out_dir = os.path.join(os.path.dirname(ledger_path), "mongodb_export")
                os.makedirs(out_dir, exist_ok=True)
                export_path = os.path.join(out_dir, "blockchain_ledger.json")
                with open(export_path, "w", encoding="utf-8") as ef:
                    json.dump(ledger, ef, indent=2)
                return {"success": True, "count": len(ledger), "collection": "blockchain_ledger", "exported_to": export_path, "note": "Offline JSON backup saved"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def sync_all_files(self, root_dir: str) -> Dict[str, Any]:
        records = []
        ignore_dirs = {".venv", ".git", "__pycache__", ".idea", ".vscode"}
        ignore_exts = {".pyc", ".pyd"}

        for r, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ignore_exts:
                    continue
                full_path = os.path.join(r, file)
                rel_path = os.path.relpath(full_path, root_dir)
                try:
                    stat = os.stat(full_path)
                    is_text = ext in [".py", ".json", ".txt", ".md", ".bat", ".toml", ".gitignore"]
                    content = ""
                    if is_text:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                    with open(full_path, "rb") as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()

                    record = {
                        "filename": file,
                        "relative_path": rel_path.replace("\\", "/"),
                        "extension": ext,
                        "size_bytes": stat.st_size,
                        "modified_at": stat.st_mtime,
                        "sha256": file_hash,
                        "is_text": is_text,
                        "content": content if is_text else "[Binary Asset]",
                        "synced_at": time.time()
                    }
                    records.append(record)
                except Exception:
                    pass

        if self.is_connected and self.db is not None:
            col = self.db["project_files"]
            col.delete_many({})
            if records:
                col.insert_many(records)
            return {"success": True, "count": len(records), "collection": "project_files", "status": "MongoDB Live Sync"}
        else:
            out_dir = os.path.join(root_dir, "data", "mongodb_export")
            os.makedirs(out_dir, exist_ok=True)
            export_path = os.path.join(out_dir, "project_files.json")
            with open(export_path, "w", encoding="utf-8") as ef:
                json.dump(records, ef, indent=2)
            return {"success": True, "count": len(records), "collection": "project_files", "exported_to": export_path, "status": "Offline Export Ready for Mongo Import"}

    def get_status(self) -> Dict[str, Any]:
        if not self.is_connected or self.db is None:
            return {"connected": False, "uri": self.uri, "collections": {}}
        try:
            stats = {}
            for col_name in self.db.list_collection_names():
                stats[col_name] = self.db[col_name].count_documents({})
            return {"connected": True, "uri": self.uri, "collections": stats}
        except Exception as e:
            return {"connected": False, "error": str(e)}

if __name__ == "__main__":
    mgr = MongoDBManager()
    print("MongoDB status:", mgr.get_status())
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    k_path = os.path.join(base_dir, "data", "ai_knowledge_226.json")
    l_path = os.path.join(base_dir, "data", "blockchain_ledger.json")
    print("Knowledge sync:", mgr.sync_knowledge_base(k_path))
    print("Blockchain sync:", mgr.sync_blockchain_ledger(l_path))
    print("Project files sync:", mgr.sync_all_files(base_dir))

