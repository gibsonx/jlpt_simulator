import os
import pymongo
from dotenv import load_dotenv
from random import randint

load_dotenv()

# ----------------------------------------------------------------------------------------------------------
CONNECTION_STRING = os.environ['AZURE_MONGO_CONNECTION']
DB_NAME = "api-mongodb-sample-database"
UNSHARDED_COLLECTION_NAME = "unsharded-sample-collection"
SAMPLE_FIELD_NAME = "sample_field"

def delete_document(collection, document_id):
    """Delete the document containing document_id from the collection"""
    collection.delete_one({"_id": document_id})
    print(f"Deleted document with _id {document_id}")

def read_document(collection, document_id):
    """Return the contents of the document containing document_id"""
    doc = collection.find_one({"_id": document_id})
    print(f"Found a document with _id {document_id}: {doc}")

def update_document(collection, document_id):
    """Update the sample field value in the document containing document_id"""
    collection.update_one({"_id": document_id}, {"$set": {SAMPLE_FIELD_NAME: "Updated!"}})
    doc = collection.find_one({"_id": document_id})
    print(f"Updated document with _id {document_id}: {doc}")

def insert_sample_document(collection):
    """Insert a sample document and return the contents of its _id field"""
    document_id = collection.insert_one({SAMPLE_FIELD_NAME: randint(50, 500)}).inserted_id
    print(f"Inserted document with _id {document_id}")
    return document_id

def create_database_unsharded_collection(client):
    """Create sample database and unsharded collection (serverless compatible)"""
    db = client[DB_NAME]

    # Create collection if it doesn't exist
    if UNSHARDED_COLLECTION_NAME not in db.list_collection_names():
        db.create_collection(UNSHARDED_COLLECTION_NAME)
        print(f"Created collection {UNSHARDED_COLLECTION_NAME}")

    return db[UNSHARDED_COLLECTION_NAME]

def main():
    """Connect to Cosmos DB Mongo API, create DB and collection, perform CRUD operations"""
    client = pymongo.MongoClient(CONNECTION_STRING)

    try:
        client.server_info()  # validate connection string
    except pymongo.errors.ServerSelectionTimeoutError:
        raise TimeoutError("Invalid API for MongoDB connection string or timed out when attempting to connect")

    collection = create_database_unsharded_collection(client)
    document_id = insert_sample_document(collection)

    read_document(collection, document_id)
    update_document(collection, document_id)
    delete_document(collection, document_id)

if __name__ == "__main__":
    main()
