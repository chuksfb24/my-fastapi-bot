import os
import asyncio
import urllib.parse  # 1. Import the URL parsing library
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(title="Bot Dashboard App with DB")

MONGO_URI = os.environ.get("MONGO_URI")
db = None

async def start_bot_background():
    print("🤖 Bot background loop initiated...")
    await asyncio.sleep(2)
    if db is not None:
        logs_collection = db["bot_logs"]
        await logs_collection.insert_one({"event": "Bot started", "timestamp": "2026-10-13"})
        print("💾 Initial boot log saved permanently to MongoDB cloud!")
    while True:
        await asyncio.sleep(3600) 

@app.on_event("startup")
async def startup_event():
    """Triggers automatically when Render boots up the web container."""
    global db
    if MONGO_URI:
        try:
            # 2. Automatically fix special characters in the connection string
            # This safely encodes passwords containing @, :, /, +, etc.
            parsed_uri = urllib.parse.urlparse(MONGO_URI)
            if parsed_uri.password:
                encoded_password = urllib.parse.quote_plus(parsed_uri.password)
                # Reconstruct the URI with the safely escaped password
                safe_uri = MONGO_URI.replace(parsed_uri.password, encoded_password)
            else:
                safe_uri = MONGO_URI

            # Connect using the corrected string
            client = AsyncIOMotorClient(safe_uri)
            db = client["my_bot_database"]
            print("🔗 Connected successfully to MongoDB Atlas Cloud!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    else:
        print("⚠️ MONGO_URI missing! Running without database persistence.")

    asyncio.create_task(start_bot_background())

@app.get("/", response_class=HTMLResponse)
async def home_dashboard():
    return "🚀 Web App Dashboard - Running"
