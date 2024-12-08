import subprocess
import time
from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId

def port_forward(namespace, pod_name, local_port, remote_port):
    """
    Starts port-forwarding using kubectl.
    """
    cmd = [
        "kubectl", "port-forward", 
        f"pod/{pod_name}", 
        f"{local_port}:{remote_port}", 
        "-n", namespace
    ]
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def download_file_from_mongodb(local_port, database_name, file_id, output_path):
    mongo_uri = f"mongodb://localhost:{local_port}/?directConnection=true"

    print(f"Connecting to MongoDB at: {mongo_uri}")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        print("MongoDB connection successful:", client.server_info())
    except Exception as e:
        print("Error connecting to MongoDB:", e)
        return

    db = client[database_name]
    fs = GridFS(db)

    try:
        file_id = ObjectId(file_id)
        file_data = fs.find_one({"_id": file_id})
        if file_data:
            with open(output_path, "wb") as f:
                f.write(file_data.read())
            print(f"File downloaded successfully to {output_path}")
        else:
            print(f"File with _id '{file_id}' not found.")
    except Exception as e:
        print("Error during file retrieval:", e)

def main():
    namespace = "default"  # Replace with your namespace
    pod_name = "mongodb-0"  # Replace with your MongoDB pod name
    local_port = 27017
    remote_port = 27017
    database_name = "mp3s"  # Replace with your MongoDB database name
    file_id = "6752eeb526799c05f6a46bed"  # Replace with the name of the file to download
    output_path = f"./{file_id}.mp3"  # Local path to save the downloaded file

    # Step 1: Start port-forwarding
    print("Starting port-forwarding...")
    port_forward_process = port_forward(namespace, pod_name, local_port, remote_port)

    try:
        # Wait a few seconds to ensure port-forwarding is ready
        time.sleep(5)

        # Step 2: Download the file
        print("Downloading file from MongoDB...")
        download_file_from_mongodb(local_port, database_name, file_id, output_path)
    finally:
        # Step 3: Stop port-forwarding
        print("Stopping port-forwarding...")
        port_forward_process.terminate()
        port_forward_process.wait()
        print("Port-forwarding stopped.")

if __name__ == "__main__":
    main()

