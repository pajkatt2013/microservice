import jwt, datetime, os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import logging

server = Flask(__name__)
mysql = MySQL(server)

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

@server.route("/login", methods = ["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "missing credentials", 401
    
    #check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute("select email,password from user where email = %s",(auth.username,))
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password :
            return "invalid credencials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credencials", 401
# Configure logging
logging.basicConfig(level=logging.INFO)

@server.route("/validate", methods = ["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]
    if not encoded_jwt:
        
        logging.warning("Authorization header is missing.")
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms = ["HS256"]
        )
    
        logging.info(f"JWT decoded successfully: {decoded}")
        return decoded, 200
    # except:
    #     return "not authorized", 403
    except jwt.ExpiredSignatureError:
        logging.error("JWT has expired.")
        return jsonify({"error": "token has expired"}), 403

    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
        return jsonify({"error": "not authorized"}), 403

    except Exception as e:
        logging.exception(f"An unexpected error occurred: {e}")
        return jsonify({"error": "internal server error"}), 500



def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz = datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(tz = datetime.timezone.utc),
            "admin": authz,
        },
        secret,
        algorithm = "HS256",
    )

if __name__ == "__main__":
    server.run(host = "0.0.0.0", port=5000)
