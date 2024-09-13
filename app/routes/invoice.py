from fastapi import APIRouter, HTTPException, Depends,Request
from app.schemas import InvoiceRequest
from app.utils.pdf_generator import generate_pdf
from app.models import consumption_collection, invoices_collection
from datetime import datetime
from fastapi.responses import StreamingResponse
from app.utils.auth_utils import get_current_user
router = APIRouter()


def calculate_bill(units: int, invoice_date: datetime) -> float:
    base_rate = 0.12
    if units <= 100:
        bill = units * base_rate
    elif units <= 200:
        bill = 100 * base_rate + (units - 100) * 0.15
    elif units <= 300:
        bill = 100 * base_rate + 100 * 0.15 + (units - 200) * 0.20
    else:
        bill = 100 * base_rate + 100 * 0.15 + 100 * 0.20 + (units - 300) * 0.25

    bill += 20  # Fixed charge
    if units > 500:
        bill *= 1.10  # 10% surcharge

    tax = bill * 0.18
    bill += tax

    # Late Payment Penalty
    penalty = 0
    if (datetime.utcnow() - invoice_date).days > 10:
        penalty = 0.02 * bill
        bill += penalty

    return bill


@router.post("/invoice")
async def generate_invoice(data: InvoiceRequest, request: Request, user: dict = Depends(get_current_user)):

    username = user.get("username")

    if not username:
        raise HTTPException(status_code=401, detail="User not found in token")

    consumption = consumption_collection.find_one({"username": username, "month": data.month})
    if not consumption:
        raise HTTPException(status_code=404, detail="Consumption data not found")

    invoice = invoices_collection.find_one({"username": username, "month": data.month})
    if invoice:
        raise HTTPException(status_code=400, detail="Invoice already generated")

    units = consumption["units_consumed"]
    total_amount = calculate_bill(units, datetime.utcnow())

    pdf_content = f"""
    Username: {username}
    Month: {data.month}
    Units Consumed: {units}
    Total Amount: ${total_amount:.2f}
    """

    pdf = generate_pdf(pdf_content)

    invoice_id = invoices_collection.insert_one({
        "username": username,
        "month": data.month,
        "total_amount": total_amount,
        "invoice_pdf_url": "",  # URL for the generated PDF if stored
        "generated_at": datetime.utcnow(),
        "paid": False
    }).inserted_id


    pdf_url = "URL_OF_THE_PDF" #need to store in cloud or db not implemented for now
    invoices_collection.update_one({"_id": invoice_id}, {"$set": {"invoice_pdf_url": pdf_url}})

    return StreamingResponse(pdf, media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=invoice.pdf"})
