from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ActivityTypes, Attachment, Activity
import os
import json
import datetime

# ✅ Глобальные переменные для инструкций и времени последней загрузки
INSTRUCTIONS = {}
LAST_LOADED = None

# ✅ Функция загрузки инструкций из папки
def load_instructions(directory="instructions"):
    global INSTRUCTIONS, LAST_LOADED

    current_dir = os.path.dirname(os.path.abspath(__file__))
    instructions_dir = os.path.join(current_dir, directory)

    print(f"[ℹ] Перезагрузка инструкций из: {instructions_dir}")

    if not os.path.exists(instructions_dir):
        print(f"[❗ Ошибка] Папка инструкций не найдена: {instructions_dir}")
        INSTRUCTIONS = {}
        return

    instructions = {}
    for filename in os.listdir(instructions_dir):
        if filename.endswith(".json"):
            key = filename.replace("_", " ").replace(".json", "").lower()
            file_path = os.path.join(instructions_dir, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    instructions[key] = json.load(f)
                    print(f"[✅ Загружено] {key} из {file_path}")
            except Exception as e:
                print(f"[❗ Ошибка чтения] {file_path}: {e}")

    INSTRUCTIONS = instructions
    LAST_LOADED = datetime.datetime.now()
    print(f"[✅ Инструкции перезагружены в {LAST_LOADED}]")

# ✅ Инициализация инструкций при запуске
load_instructions()

# ✅ Основной класс бота
class ITSupportBot(ActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            await self.on_message_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            await self.on_members_added_activity(turn_context.activity.members_added, turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower() if turn_context.activity.text else ""
        print(f"➡ Benutzer sagte: {text}")

        if not text or text == "menu":
            await self._send_main_menu_adaptive(turn_context)
            return

        if text == "reload":
            load_instructions()
            await turn_context.send_activity(f"🔄 Инструкции перезагружены ({LAST_LOADED})")
            return

        if text in INSTRUCTIONS:
            await self._send_instruction_adaptive(turn_context, text)
        else:
            await self._send_main_menu_adaptive(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Willkommen beim IT Support Bot! Tippe 'menu' um zu starten.")

    async def _send_main_menu_adaptive(self, turn_context: TurnContext):
        buttons = []
        for key, instr in INSTRUCTIONS.items():
            buttons.append({
                "type": "Action.Submit",
                "title": instr.get("title", key.title()),
                "data": {"msteams": {"type": "messageBack", "text": key}}
            })

        card_json = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": "IT Support Menü",
                    "weight": "Bolder",
                    "size": "Large",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": "Bitte wählen Sie ein Problem aus:",
                    "wrap": True
                }
            ],
            "actions": buttons
        }

        await turn_context.send_activity(Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.adaptive",
                content=card_json
            )]
        ))

    async def _send_instruction_adaptive(self, turn_context: TurnContext, problem_key: str):
        data = INSTRUCTIONS.get(problem_key)
        if not data:
            await turn_context.send_activity("Anleitung nicht gefunden.")
            return

        steps_text = "\n\n".join([f"**Schritt {i+1}:** {step}" for i, step in enumerate(data.get("steps", []))])

        card_json = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.4",
            "body": [
                {
                    "type": "TextBlock",
                    "text": data.get("title", ""),
                    "weight": "Bolder",
                    "size": "Large",
                    "wrap": True
                },
                {
                    "type": "TextBlock",
                    "text": steps_text,
                    "wrap": True
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Zurück zum Hauptmenü",
                    "data": {"msteams": {"type": "messageBack", "text": "menu"}}
                }
            ]
        }

        if "image" in data:
            card_json["body"].insert(1, {
                "type": "Image",
                "url": data["image"],
                "size": "Stretch",
                "style": "Person"
            })

        if "related" in data:
            card_json["actions"].append({
                "type": "Action.Submit",
                "title": "VPN Anleitung anzeigen",
                "data": {"msteams": {"type": "messageBack", "text": data["related"]}}
            })

        await turn_context.send_activity(Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.adaptive",
                content=card_json
            )]
        ))

