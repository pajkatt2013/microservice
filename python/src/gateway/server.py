import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from io import BytesIO
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Logging is working!")

server = Flask(__name__)
# server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"
# mongo = PyMongo(server)
mongo_video = PyMongo(server,uri = "mongodb://mongodb-0.mongodb.default.svc.cluster.local:27017,mongodb-1.mongodb.default.svc.cluster.local:27017,mongodb-2.mongodb.default.svc.cluster.local:27017/videos?replicaSet=rs0")
mongo_mp3 = PyMongo(server,uri = "mongodb://mongodb-0.mongodb.default.svc.cluster.local:27017,mongodb-1.mongodb.default.svc.cluster.local:27017,mongodb-2.mongodb.default.svc.cluster.local:27017/mp3s?replicaSet=rs0")

# fs = gridfs.GridFS(mongo.db)
fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)
try:
    # connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq.default.svc.cluster.local'))
    channel = connection.channel()
    logging.info("succeeded in connecting to rabbitmq channel")
except pika.exceptions.AMQPError as e:
    logging.error(f"Failed to connect to RabbitMQ: {e}")

@server.route("/login", methods = ["POST"])
def login():
    token, err = access.login(request)
    if not err:
        return token
    else:
        return err
    

@server.route("/upload", methods = ["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return err
    logging.info("jwt provided in this request is validated")
    access = json.loads(access)
    

    if access["admin"]:
        if len(request.files) != 1:
            return "exactly 1 file required", 400
        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access) #files, gridfs instances,rabbitmq channel，如果没有错误，返回None
            if err:
                logging.info(f"upload failure:{err}")
                return err 
        
        return "upload successful!", 200
    else:
        return "not authorized", 401

@server.route("/download", methods = ["GET"])
def download():
    access, err = validate.token(request)
    if err:
        return err
    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")
        if not fid_string:
            return "fid is required", 400
        try:
            grid_out = fs_mp3s.get(ObjectId(fid_string))
            file_data = grid_out.read()
            file_stream = BytesIO(file_data)
            return send_file(file_stream, download_name = f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500
    else:
        return "not authorized", 401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)

