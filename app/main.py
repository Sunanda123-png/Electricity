from fastapi import FastAPI
from app.routes import auth, consumption, invoice, admin

app = FastAPI()



app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(consumption.router, prefix="/consumption", tags=["Consumption"])
app.include_router(invoice.router, prefix="/invoice", tags=["Invoice"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
