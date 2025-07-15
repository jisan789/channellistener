import asyncio
from fastapi import FastAPI
from telethon import TelegramClient
from telethon.sessions import StringSession
from fastapi.responses import JSONResponse

api_id = 28345038
api_hash = '6c438bbc256629655ca14d4f74de0541'
string_session = ''  # Your session string here
channel_id = -1002704490894

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Telegram Listener API running"}

@app.get("/")
async def start_listen():
    # Initialize client per request
    client = TelegramClient(StringSession(string_session), api_id, api_hash)
    await client.start()

    # Find channel entity
    dialogs = await client.get_dialogs()
    target_channel = None
    for dialog in dialogs:
        if dialog.id == channel_id:
            target_channel = dialog.entity
            break

    if not target_channel:
        await client.disconnect()
        return JSONResponse(status_code=404, content={"error": "Channel not found or you're not a member."})

    # Fetch last 2 messages
    messages = await client.get_messages(target_channel, limit=2)

    recent_posts = []
    for msg in messages:
        recent_posts.append({
            "id": msg.id,
            "text": msg.text or msg.message or "",
            "date": str(msg.date)
        })

    await client.disconnect()

    return {
        "message": "Fetched recent 2 posts.",
        "recent_posts": recent_posts
    }
