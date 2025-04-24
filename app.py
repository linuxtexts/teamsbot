from botbuilder.core import ActivityHandler, TurnContext

class ITSupportBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.strip().lower()

        if "password" in text:
            await turn_context.send_activity("You can reset your password using the company portal.")
        elif "install" in text or "software" in text:
            await turn_context.send_activity("Please contact IT for software installation or check the IT portal.")
        elif "network" in text or "wifi" in text:
            await turn_context.send_activity("Try restarting your router. If the issue continues, contact the IT desk.")
        else:
            await turn_context.send_activity("Sorry, I didn't get that. Can you ask in a different way?")

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hi! I'm your IT Support Bot. How can I help you today?")
