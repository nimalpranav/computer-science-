import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"classroom_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        print(f"✅ Connected to room {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        is_voice = data.get("is_voice", False)

        # Support voice_blob (Base64) if sent
        if not message and "voice_blob" in data:
            message = data["voice_blob"]
            is_voice = True

        if not message:
            return  # ignore empty messages

        print("📩 Received:", message)

        # Broadcast to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "is_voice": is_voice
            }
        )

    async def chat_message(self, event):
        message = event.get("message")
        if not message:
            return

        print("📤 Sending:", message)

        # Send to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "is_voice": event.get("is_voice", False)
        }))
