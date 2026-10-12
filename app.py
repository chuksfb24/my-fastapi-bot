import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(title="Bot Dashboard App with DB")

# 1. Read the hidden Connection String from Render's Environment Variables
MONGO_URI = os.environ.get("MONGO_URI")
db = None

async def start_bot_background():
    """Your background bot loop that interacts with the cloud database."""
    print("🤖 Bot background loop initiated...")
    
    # Wait a moment for the database to establish a connection
    await asyncio.sleep(2)
    
    if db is not None:
        # Example: Save a configuration or log to the database
        logs_collection = db["bot_logs"]
        await logs_collection.insert_one({"event": "Bot started", "timestamp": "2026-10-12"})
        print("💾 Initial boot log saved permanently to MongoDB cloud!")
        
        # Example: Count total logged items
        count = await logs_collection.count_documents({})
        print(f"📊 Total saved logs in database: {count}")

    while True:
        await asyncio.sleep(3600) 

@app.on_event("startup")
async def startup_event():
    """Triggers automatically when Render boots up the web container."""
    global db
    if MONGO_URI:
        try:
            # Connect asynchronously to your MongoDB Atlas cluster
            client = AsyncIOMotorClient(MONGO_URI)
            db = client["my_bot_database"]
            print("🔗 Connected successfully to MongoDB Atlas Cloud!")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
    else:
        print("⚠️ MONGO_URI missing! Running without database persistence.")

    asyncio.create_task(start_bot_background())

@app.get("/", response_class=HTMLResponse)
async def home_dashboard():
    return """
    <html>
        <head><title>Dashboard</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 50px;">
            <h2>🚀 Web App Dashboard</h2>
            <p>Database Connectivity: <strong>Enabled & Persistent</strong></p>
        </body>
    </html>
    """
