from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

def fetch_file_from_gridfs(db_name, collection_name, file_id, local_filename):
    try:
        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")  # Change this to your MongoDB connection string if needed
        db = client[db_name]
        
        # Create a GridFS object
        fs = GridFS(db, collection=collection_name)
        
        # Fetch the file by ObjectId
        grid_out = fs.get(ObjectId(file_id))
        
        # Write the file to the local filesystem
        with open(local_filename, 'wb') as local_file:
            local_file.write(grid_out.read())
        
        print(f"File saved as {local_filename}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    db_name = "mp3s"  # Database name
    collection_name = "fs"  # GridFS default collection name is 'fs', but change if yours is different
    file_id = "66d518fa834f3902389dd35d"  # The ObjectId of the file in GridFS
    local_filename = "test.mp3"  # The local filename where the file will be saved
    
    fetch_file_from_gridfs(db_name, collection_name, file_id, local_filename)