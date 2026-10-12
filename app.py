import os
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# Initialize FastAPI Web App
app = FastAPI(title="Bot Dashboard App")

async def start_bot():
    """Background loop representing your bot framework's main process."""
    print("🤖 Bot initialization sequence started...")
    while True:
        # This keeps the background process alive. Replace this with your actual bot polling/start logic.
        # e.g., await bot.start(os.environ.get("BOT_TOKEN"))
        await asyncio.sleep(3600) 

@app.on_event("startup")
async def startup_event():
    """Triggers automatically when the web app boots up on Render."""
    asyncio.create_task(start_bot())

@app.get("/", response_class=HTMLResponse)
async def home_dashboard():
    """The public URL homepage that users (and pinging services) will see."""
    return """
    <html>
        <head>
            <title>Application Status Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; background: #f4f6f9; color: #333; }
                .card { background: white; padding: 30px; display: inline-block; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; }
                .status { color: #2ecc71; font-weight: bold; }
                .instructions { text-align: left; background: #eee; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🚀 Web App Dashboard</h1>
                <p>Application Status: <span class="status">ONLINE (24/7)</span></p>
                <p>The web front-end and your background bot process are running concurrently.</p>
                <hr>
                <h3>Render Configuration Reference</h3>
                <div class="instructions">
                    <strong>Build Command:</strong> pip install -r requirements.txt<br>
                    <strong>Start Command:</strong> uvicorn app:app --host 0.0.0.0 --port $PORT
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/healthz")
async def health_check():
    """A lightweight endpoint optimized specifically for automated uptime pingers."""
    return {"status": "healthy", "bot_running": True}
