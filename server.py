from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity
from app import ITSupportBot
import os

# Настройки адаптера без авторизации
adapter_settings = BotFrameworkAdapterSettings("", "")
adapter_settings.disable_authentication = True
adapter = BotFrameworkAdapter(adapter_settings)

# Создаем экземпляр бота
bot = ITSupportBot()

# Обработчик сообщений
async def handle_message(turn_context: TurnContext):
    if turn_context.activity.type == "message":
        await bot.on_message_activity(turn_context)
    elif turn_context.activity.type == "conversationUpdate":
        if turn_context.activity.members_added:
            await bot.on_members_added_activity(turn_context.activity.members_added, turn_context)
    else:
        print(f"🔄 Игнорируем тип активности: {turn_context.activity.type}")

# Обработчик /api/messages
async def messages(req: web.Request) -> web.Response:
    print("🚨 Запрос получен на /api/messages!")
    try:
        body = await req.json()
        activity = Activity().deserialize(body)
        async def aux_func(turn_context):
            await handle_message(turn_context)
        await adapter.process_activity(activity, "", aux_func)
        return web.Response(status=200)
    except Exception as e:
        print(f"❌ Ошибка в обработке запроса: {e}")
        return web.Response(status=500, text=str(e))

# Проверка / корневой маршрут
async def root(req):
    return web.Response(text="✅ IT Support Bot активен! Сервер работает.")

# Создание и настройка приложения
app = web.Application()

# Добавляем поддержку статических файлов
app.router.add_static('/images/', path=os.path.join(os.path.dirname(__file__), 'images'))

app.router.add_get("/", root)
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    try:
        web.run_app(app, host="localhost", port=3978)
    except Exception as e:
        print(f"❌ Ошибка запуска сервера: {e}")

