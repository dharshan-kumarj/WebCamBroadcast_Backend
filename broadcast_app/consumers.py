import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class SignalingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.room_group_name = f'webrtc_{self.stream_id}'
        
        logger.info(f"WebRTC signaling connection attempt for stream: {self.stream_id}")
        
        try:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"WebRTC signaling connection accepted for stream: {self.stream_id}")
        except Exception as e:
            logger.error(f"WebRTC signaling connect error: {str(e)}")
            raise
    
    async def disconnect(self, close_code):
        # Leave room group
        logger.info(f"WebRTC signaling disconnected: {self.stream_id}, code: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            logger.info(f"Received WebRTC signaling: {message_type}")
            
            # Forward the signaling message to the room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'relay_message',
                    'message': data,
                    'sender_channel_name': self.channel_name
                }
            )
        except Exception as e:
            logger.error(f"Error in WebRTC signaling receive: {str(e)}")
    
    # Relay WebRTC messages to other clients
    async def relay_message(self, event):
        message = event['message']
        sender_channel_name = event['sender_channel_name']
        
        # Don't send the message back to the sender
        if sender_channel_name != self.channel_name:
            await self.send(text_data=json.dumps(message))