from fastapi import FastAPI
from telethon import TelegramClient
from telethon.sessions import StringSession
from fastapi.responses import JSONResponse

api_id = 28345038
api_hash = '6c438bbc256629655ca14d4f74de0541'
string_session = '1BVtsOHEBu7Ps0EP0Sf__DVSXwT5fI5EAW_XNszWyjecxwwtpq2FPkIBxs-6oxsnquDhS8txn2RLSlPtJhv124hKlLZ1Qfeg46sOzmWtcFb4s17ANgysjABnx6VNFcBrzzEqpP0TqRhOSH2BwnyniyaW7cvjcvBsW1JJiQUXddxqqb9DeamEcPB9KNsjf9gLIeWRJ9aLg14Lj5j81tWd3ylh7E2r-R4WutrcBs3ed-Bl5V6_laWPnoy8IiTE0rRdZ5guAO8JOLdn3dwyGAu1NbYru6_NrloqSx9Shod9gtr8pQk5le_KHCWhtqfUrQqClqnQo2axKolIOk3gTHFoDZOGJvJ2eiPM='  # Insert your valid string session here
channel_id = -1002039265615

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
