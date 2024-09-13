from pymongo import MongoClient
from app.config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client.electricity_billing

# Define collections
users_collection = db.users
consumption_collection = db.consumption
invoices_collection = db.invoices
