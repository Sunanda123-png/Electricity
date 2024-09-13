import bcrypt
import jwt
from app.config import SECRET_KEY
from datetime import datetime, timedelta
from app.models import users_collection
from typing import Optional
from fastapi import Request, HTTPException
from typing import Dict
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(stored_password: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))

def create_jwt_token(username: str) -> str:
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm="HS256")


def decode_jwt_token(token: str) -> Optional[Dict[str, any]]:
    try:
        # Remove the Bearer prefix if present
        if token.startswith("Bearer "):
            token = token[len("Bearer "):]

        # Decode the token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def get_user_role(token: str) -> Optional[str]:
    print(f"Token received: {token}")  # Debug: Print the token

    # Decode the JWT token
    payload = decode_jwt_token(token)
    print(f"Decoded payload: {payload}")  # Debug: Print the payload

    # Check if payload is not None and contains the 'sub' key
    if payload and "sub" in payload:
        # Retrieve user from database
        user = users_collection.find_one({"username": payload["sub"]})
        print(f"User found: {user}")  # Debug: Print the user document

        if user:
            # Return the role if it exists in the user document
            return user.get("role")

    # Return None if no role is found or if user does not exist
    return None

def get_current_user(request: Request):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    payload = decode_jwt_token(token)
    if payload:
        user = users_collection.find_one({"username": payload["sub"]})
        if user:
            return user
    raise HTTPException(status_code=401, detail="Invalid token")