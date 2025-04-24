from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
import asyncio
from app import ITSupportBot

app = Flask(__name__)

# App ID and password (empty for local testing in Emulator)
APP_ID = ""
APP_PASSWORD = ""

# Adapter settings
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# Create bot
bot = ITSupportBot()

# Handle messages at /api/messages
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def aux():
        await adapter.process_activity(activity, auth_header, bot.on_turn)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(aux())
        return Response(status=202)
    except Exception as e:
        print(f"Exception: {e}")
        return Response(status=500)

if __name__ == "__main__":
    app.run(port=3978)

