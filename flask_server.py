from flask import Flask, request, Response
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from app import ITSupportBot

import asyncio

# Настройки адаптера (без авторизации — только для разработки)
adapter_settings = BotFrameworkAdapterSettings("", "")
adapter_settings.disable_authentication = True
adapter = BotFrameworkAdapter(adapter_settings)

bot = ITSupportBot()

app = Flask(__name__)
loop = asyncio.get_event_loop()

# Обработчик сообщений
async def handle_message(turn_context: TurnContext):
    if turn_context.activity.type == "message":
        await bot.on_message_activity(turn_context)
    elif turn_context.activity.type == "conversationUpdate":
        if turn_context.activity.members_added:
            await bot.on_members_added_activity(turn_context.activity.members_added, turn_context)
    else:
        print(f"🔄 Игнорируем тип активности: {turn_context.activity.type}")

@app.route("/", methods=["GET"])
def index():
    return "✅ IT Support Bot активен! Flask работает."

@app.route("/api/messages", methods=["POST"])
def messages():
    try:
        activity = Activity().deserialize(request.json)

        async def aux_func(turn_context):
            await handle_message(turn_context)

        task = loop.create_task(adapter.process_activity(activity, "", aux_func))
        loop.run_until_complete(task)

        return Response(status=200)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return Response(f"Error: {e}", status=500)
