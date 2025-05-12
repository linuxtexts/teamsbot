from flask import Flask, request, Response
from flask_cors import CORS
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from app import ITSupportBot
import asyncio

app = Flask(__name__)
CORS(app)

from flask import send_from_directory
import os

@app.route("/images/<path:filename>")
def serve_image(filename):
    # Полный путь к /home/remtel/teamsbot/images
    image_dir = "/home/remtel/teamsbot/images"
    return send_from_directory(image_dir, filename)

adapter_settings = BotFrameworkAdapterSettings("microsoft-id", "password")
adapter = BotFrameworkAdapter(adapter_settings)
bot = ITSupportBot()

# 🟢 СНАЧАЛА определяем функцию:
async def handle_message(turn_context: TurnContext):
    if turn_context.activity.type == "message":
        await bot.on_message_activity(turn_context)
    elif turn_context.activity.type == "conversationUpdate":
        if turn_context.activity.members_added:
            await bot.on_members_added_activity(turn_context.activity.members_added, turn_context)

# 🔵 ПОТОМ используем её:
@app.route("/api/messages", methods=["POST", "OPTIONS"])
def messages():
    if not request.is_json:
        return Response("Unsupported Media Type", status=415)

    try:
        activity = Activity().deserialize(request.json)

        async def aux_func(turn_context):
            await handle_message(turn_context)

        asyncio.run(adapter.process_activity(
            activity,
            request.headers.get("Authorization", ""),
            aux_func
        ))

        return Response(status=200)

    except Exception as e:
        print(f"❌ Ошибка обработки: {e}")
        return Response(f"Error: {e}", status=500)
