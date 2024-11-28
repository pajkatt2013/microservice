import jwt
import datetime

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
# Example usage:
username = "john.doe"
secret = "your_secret_key"
authz = True  # User has admin privileges

token = createJWT(username, secret, authz)

print(token)  # Output: the encoded JWT