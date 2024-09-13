from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ConsumptionData
from app.models import consumption_collection
from datetime import datetime
from app.utils.auth_utils import get_current_user

router = APIRouter()


@router.post("/consumption")
async def add_consumption(data: ConsumptionData, user: dict = Depends(get_current_user)):
    existing_data = consumption_collection.find_one({"username": user["username"], "month": data.month})
    if existing_data:
        raise HTTPException(status_code=400, detail="Consumption data for this month already exists")

    try:
        datetime.strptime(data.month, "%Y-%m")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid month format. Use YYYY-MM")

    if data.units_consumed <= 0:
        raise HTTPException(status_code=400, detail="Units consumed must be a positive number")

    consumption_collection.insert_one({
        "username": user["username"],
        "month": data.month,
        "units_consumed": data.units_consumed
    })

    return {"msg": "Consumption data added successfully"}
