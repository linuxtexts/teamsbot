from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ActivityTypes, CardAction, HeroCard, ActionTypes, AttachmentLayoutTypes, Attachment, Activity, ActivityTypes, CardImage
from typing import List

class ITSupportBot(ActivityHandler):
    async def on_turn(self, turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            await self.on_message_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            await self.on_members_added_activity(
                turn_context.activity.members_added, turn_context
            )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower() if turn_context.activity.text else ""
        print(f"➡ Benutzer sagte: {text}")

        if not text or text == "menu":
            await self._send_main_menu(turn_context)
            return

        if text == "vpn problem":
            await self._send_vpn_instructions(turn_context)
        elif text == "sap passwort problem":
            await self._send_sap_instructions(turn_context)
        elif text == "email problem":
            await self._send_email_instructions(turn_context)
        else:
            await self._send_main_menu(turn_context)

    async def on_members_added_activity(self, members_added, turn_context: TurnContext):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                print("👋 Neuer Benutzer ist beigetreten")
                await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        card = HeroCard(
            title="Willkommen beim IT Support Bot!",
            subtitle="Wie kann ich Ihnen helfen?",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="Zum Menü",
                    value="menu"
                )
            ]
        )
        reply = Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card
            )]
        )
        await turn_context.send_activity(reply)

    async def _send_main_menu(self, turn_context: TurnContext):
        card = HeroCard(
            title="IT Support Menü",
            text="Bitte wählen Sie ein Problem aus:",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="VPN Problem",
                    value="vpn problem"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="SAP Passwort Problem",
                    value="sap passwort problem"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="E-Mail Problem auf dem Handy",
                    value="email problem"
                )
            ]
        )
        reply = Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card
            )]
        )
        await turn_context.send_activity(reply)

    async def _send_vpn_instructions(self, turn_context: TurnContext):
        # Отправляем первые два шага
        card1 = HeroCard(
            title="VPN Problemlösung",
            text="""**Schritt 1:** Starten Sie Ihren Laptop neu\n\n
**Schritt 2:** Öffnen Sie den Browser und klicken Sie auf das Symbol in der unteren rechten Ecke (Global Protect):""",
        )
        await turn_context.send_activity(Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card1
            )]
        ))

        # Отправляем изображение
        card2 = HeroCard(
            images=[
                CardImage(
                    url="http://localhost:3978/images/global-protect-icon.png"
                )
            ]
        )
        await turn_context.send_activity(Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card2
            )]
        ))

        # Отправляем третий шаг и кнопку возврата
        card3 = HeroCard(
            text="**Schritt 3:** Klicken Sie auf 'Verbinden'",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="Zurück zum Hauptmenü",
                    value="menu"
                )
            ]
        )
        await turn_context.send_activity(Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card3
            )]
        ))

    async def _send_sap_instructions(self, turn_context: TurnContext):
        card = HeroCard(
            title="SAP Passwort Problemlösung",
            text="""**Schritt 1:** Starten Sie Ihren Laptop neu\n\n
**Schritt 2:** Prüfen Sie, ob VPN aktiviert ist""",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="VPN Anleitung anzeigen",
                    value="vpn problem"
                ),
                CardAction(
                    type=ActionTypes.im_back,
                    title="Zurück zum Hauptmenü",
                    value="menu"
                )
            ]
        )
        reply = Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card
            )]
        )
        await turn_context.send_activity(reply)

    async def _send_email_instructions(self, turn_context: TurnContext):
        card = HeroCard(
            title="E-Mail auf dem Handy Problemlösung",
            text="""**Schritt 1:** Prüfen Sie die Internetverbindung auf Ihrem Handy\n\n
**Schritt 2:** Starten Sie Defender (Symbol wird angezeigt) und führen Sie die Authentifizierung durch\n\n
**Schritt 3:** Gehen Sie zu Einstellungen --> Apps (unten) --> Mail --> Mail Accounts --> EXO --> Anmelden""",
            buttons=[
                CardAction(
                    type=ActionTypes.im_back,
                    title="Zurück zum Hauptmenü",
                    value="menu"
                )
            ]
        )
        reply = Activity(
            type=ActivityTypes.message,
            attachments=[Attachment(
                content_type="application/vnd.microsoft.card.hero",
                content=card
            )]
        )
        await turn_context.send_activity(reply)
