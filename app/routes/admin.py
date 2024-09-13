from fastapi import APIRouter, HTTPException, Depends
from app.utils.auth_utils import decode_jwt_token
from app.models import invoices_collection, users_collection
from app.utils.auth_utils import get_user_role
from typing import Optional
from fastapi import Header
from bson import ObjectId
router = APIRouter()


def get_admin_user(token: str = Header(None, alias="Authorization")) -> None:
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")

    role = get_user_role(token)

    if role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

def get_current_user(token: str) -> Optional[dict]:
    payload = decode_jwt_token(token)
    if payload and "sub" in payload:
        user = users_collection.find_one({"username": payload["sub"]})
        if user:
            return user  # Return the user document
    return None


@router.get("/invoices")
async def view_all_invoices(token: str = Header(None, alias="Authorization")):
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")


    current_user = get_current_user(token)


    if current_user["role"] == "admin":
        non_admin_users = list(users_collection.find())

        usernames = [user["username"] for user in non_admin_users]
        print(usernames, "usernames")
        for username in usernames:
            invoices = list(invoices_collection.find({"username": username}))
            for invoice in invoices:
                print(invoice)
        invoices = list(invoices_collection.find({"username": {"$in": usernames}}))
        print(f"Fetched Invoices: {invoices}")

    else:
        invoices = list(invoices_collection.find({"username": current_user["username"]}))
        print(f"Fetched User Invoices: {invoices}")


    invoice_details = []
    for invoice in invoices:
        username = invoice.get("username")
        user = users_collection.find_one({"username": username})

        if user:
            # Add invoice details along with user info
            invoice_details.append({
                "username": user["username"],
                "month": invoice.get("month"),
                "total_amount": invoice.get("total_amount"),
                "pdf_link": f"/invoices/download/{invoice['_id']}"
            })

    return {"invoices": invoice_details}