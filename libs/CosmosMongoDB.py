from pymongo import MongoClient
from uuid import uuid4
from typing import Dict, Optional
from datetime import datetime


class CosmosMongoDB:
    def __init__(self, connection_string: str, database_name: str, collection_name: str):
        """
        Initialize the CosmosMongoDB class.

        Args:
            connection_string: MongoDB connection string for Cosmos DB
            database_name: Name of the database
            collection_name: Name of the collection
        """
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.collection = self._connect_or_create_collection()

    def _connect_or_create_collection(self):
        """Connect to the database and collection (created on first insert if not exists)."""
        client = MongoClient(self.connection_string)
        db = client[self.database_name]
        collection = db[self.collection_name]
        return collection

    def _add_timestamps(self, document: Dict, is_many: bool = False):
        """Add created_at and updated_at timestamps."""
        now = datetime.utcnow()
        if is_many:
            for doc in document:
                doc.setdefault("created_at", now)
                doc.setdefault("updated_at", now)
        else:
            document.setdefault("created_at", now)
            document.setdefault("updated_at", now)

    def insert_one(self, document: Dict) -> str:
        """
        Insert a single document into the collection.

        Args:
            document: Dictionary object (matches your TypedDict structures)
        Returns:
            Inserted document ID
        """
        # Add timestamps
        self._add_timestamps(document)

        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def insert_many(self, documents: list[Dict]) -> list[str]:
        """
        Insert multiple documents into the collection.

        Args:
            documents: List of dictionary objects
        Returns:
            List of inserted document IDs
        """
        for doc in documents:
            if "_id" not in doc:
                doc["_id"] = str(uuid4())

        # Add timestamps to all documents
        self._add_timestamps(documents, is_many=True)

        result = self.collection.insert_many(documents)
        return [str(_id) for _id in result.inserted_ids]


# ----------------- Example Usage -----------------
if __name__ == "__main__":
    CONNECTION_STRING = "mongodb://<username>:<password>@<cosmos-account>.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb"
    DATABASE_NAME = "myDatabase"
    COLLECTION_NAME = "questions"

    db_client = CosmosMongoDB(CONNECTION_STRING, DATABASE_NAME, COLLECTION_NAME)

    # Insert a single question
    single_question = {
        "html_question": "<p>What is 2+2?</p>",
        "correct_answer": 2,
        "choices": ["3", "4", "5", "6"]
    }
    inserted_id = db_client.insert_one(single_question)
    print("Inserted single document ID:", inserted_id)

    # Insert multiple questions
    multiple_questions = [
        {"html_question": "<p>Capital of France?</p>", "correct_answer": 1,
         "choices": ["Paris", "London", "Berlin", "Rome"]},
        {"html_question": "<p>3*3=?</p>", "correct_answer": 3, "choices": ["6", "7", "9", "8"]}
    ]
    inserted_ids = db_client.insert_many(multiple_questions)
    print("Inserted multiple document IDs:", inserted_ids)
