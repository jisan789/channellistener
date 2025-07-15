from fastapi import FastAPI
from telethon import TelegramClient
from telethon.sessions import StringSession
from fastapi.responses import JSONResponse

api_id = 28345038
api_hash = '6c438bbc256629655ca14d4f74de0541'
string_session = '1BVtsOLUBu1crEID8o2mj9IKdivq4aifZ0-_5s6OLDWHQzlftgquIKw6Wf-zhDAiAwrYIRcCzA9XU8V5OgkWTpTfp2C5y-J13a5wpNbhGO6lCHk7rT-V3YUwVCZb855OFqFwzG5eLGW2NOYe68hlzqBA4ggfJJl69kTWz8bBQULBnsHN5d_04c-EJwvi4DpN-szfif5ZIkNN9thoMTeNpsXjVZpZheL316mXGcrbyq0ZlxPrTZ3EE9utSgfULrUobSuWhy8338mc_-ctvD5tTV8Ht2AV3kmBOOxl7rRuSqn4hXIHIoX1abJJEfGCMnLb_3geYPn_OKYJrK3sFp1walcYu-qfZjBs='  # Insert your valid string session here
channel_id = -1002704490894

app = FastAPI()

@app.get("/")
async def fetch_channel_messages():
    client = TelegramClient(StringSession(string_session), api_id, api_hash)
    await client.start()

    dialogs = await client.get_dialogs()
    target_channel = None
    for dialog in dialogs:
        if dialog.id == channel_id:
            target_channel = dialog.entity
            break

    if not target_channel:
        await client.disconnect()
        return JSONResponse(status_code=404, content={"error": "Channel not found or you're not a member."})

    messages = await client.get_messages(target_channel, limit=2)
    await client.disconnect()

    recent_posts = [{
        "id": msg.id,
        "text": msg.text or msg.message or "",
        "date": str(msg.date)
    } for msg in messages]

    return {
        "message": "Fetched recent 2 posts.",
        "recent_posts": recent_posts
    }
