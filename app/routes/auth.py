from fastapi import APIRouter, HTTPException, Depends
from app.schemas import UserRegister, UserLogin
from app.utils.auth_utils import hash_password, verify_password, create_jwt_token, decode_jwt_token
from app.models import users_collection

router = APIRouter()


@router.post("/register")
async def register(user: UserRegister):
    if users_collection.find_one({"username": user.username}) or users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed_password = hash_password(user.password)
    users_collection.insert_one({
        "username": user.username,
        "password": hashed_password,
        "email": user.email,
        "address": user.address,
        "role": user.role
    })
    return {"msg": "User registered successfully"}


@router.post("/login")
async def login(user: UserLogin):
    stored_user = users_collection.find_one({"username": user.username})
    if not stored_user or not verify_password(stored_user["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt_token(user.username)
    return {"access_token": token, "token_type": "bearer"}
