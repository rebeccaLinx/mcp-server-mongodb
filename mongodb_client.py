from motor.motor_asyncio import AsyncIOMotorClient
from typing import List, Dict, Any, Optional
from bson import ObjectId
from datetime import datetime

class MongoDBClient:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None

    def setup(self, host: str, database: str):
        """
        Setup the MongoDB connection.
        """
        uri = f"mongodb://{host}"
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[database]

    def _serialize_value(self, val: Any) -> Any:
        """
        Recursively convert ObjectId, datetime and other non-serializable types to strings.
        """
        if isinstance(val, dict):
            return {k: self._serialize_value(v) for k, v in val.items()}
        elif isinstance(val, list):
            return [self._serialize_value(v) for v in val]
        elif isinstance(val, ObjectId):
            return str(val)
        elif isinstance(val, datetime):
            return val.isoformat()
        return val

    async def get_projects(self, name: Optional[str] = None, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve projects. If name is provided, filter by name.
        """
        if self.db is None:
            return []
        
        collections = await self.db.list_collection_names()
        results = []
        
        # Projection: exclude 'data' if full is False
        projection = None if full else {"data": 0}
        
        for coll_name in collections:
            if name and coll_name != name:
                continue
                
            doc = await self.db[coll_name].find_one({"type": "project"}, projection)
            if doc:
                doc = self._serialize_value(doc)
                doc["collection_name"] = coll_name
                results.append(doc)
        return results

    async def get_assets(self, project_name: str, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve assets with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "asset", "silo": "Assets"}
        if name:
            query["name"] = name
            
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def get_sequences(self, project_name: str, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve sequences with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "sequence"}
        if name:
            query["name"] = name
            
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def get_shots(self, project_name: str, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve shots with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "asset", "silo": "Shots"}
        if name:
            query["name"] = name
            
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def get_subsets(self, project_name: str, parent_id: str, name: Optional[str] = None, limit: int = 100, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve subsets with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "subset", "parent": ObjectId(parent_id)}
        if name:
            query["name"] = name
            
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def get_versions(self, project_name: str, subset_id: str, limit: int = 10, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve versions with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "version", "parent": ObjectId(subset_id)}
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).sort("name", -1).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def get_representations(self, project_name: str, version_id: str, limit: int = 50, skip: int = 0, full: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve representations with optional full data projection.
        """
        if self.db is None:
            return []
        
        query = {"type": "representation", "parent": ObjectId(version_id)}
        projection = None if full else {"data": 0}
        cursor = self.db[project_name].find(query, projection).skip(skip).limit(limit)
        
        results = []
        async for doc in cursor:
            results.append(self._serialize_value(doc))
        return results

    async def close(self):
        """
        Close the MongoDB connection.
        """
        if self.client:
            self.client.close()
