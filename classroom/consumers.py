import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"classroom_{self.room_name}"

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ Connected to room {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        message = data.get("message")
        is_voice = data.get("is_voice", False)
        voice_blob = data.get("voice_blob")

        if voice_blob:  # voice recording
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "voice_blob": voice_blob,
                }
            )
            return

        if not message:
            return

        print("📩 Received:", message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "is_voice": is_voice
            }
        )

    async def chat_message(self, event):
        payload = {}
        if "message" in event:
            payload["message"] = event["message"]
            payload["is_voice"] = event.get("is_voice", False)
        if "voice_blob" in event:
            payload["voice_blob"] = event["voice_blob"]

        await self.send(text_data=json.dumps(payload))
