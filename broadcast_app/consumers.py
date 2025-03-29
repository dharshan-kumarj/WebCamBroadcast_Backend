import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class BroadcastConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.room_group_name = f'broadcast_{self.stream_id}'
        
        logger.info(f"WebSocket connection attempt for stream: {self.stream_id}")
        print(f"WebSocket connection attempt for stream: {self.stream_id}")  # Console log
        
        try:
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            logger.info(f"WebSocket connection accepted for stream: {self.stream_id}")
            print(f"WebSocket connection accepted for stream: {self.stream_id}")  # Console log
        except Exception as e:
            logger.error(f"WebSocket connect error: {str(e)}")
            print(f"WebSocket connect error: {str(e)}")  # Console log
            raise
    
    async def disconnect(self, close_code):
        # Leave room group
        print(f"WebSocket disconnected: {self.stream_id}, code: {close_code}")  # Console log
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')
            
            print(f"Received message type: {message_type}")  # Console log
            
            if message_type == 'video_frame':
                # Broadcast frame to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'broadcast_frame',
                        'frame': text_data_json['frame'],
                        'broadcaster_id': text_data_json.get('broadcaster_id', '')
                    }
                )
            elif message_type == 'viewer_joined':
                # Send message to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'viewer_update',
                        'action': 'joined',
                        'viewer_id': text_data_json.get('viewer_id', '')
                    }
                )
        except Exception as e:
            logger.error(f"Error in WebSocket receive: {str(e)}")
            print(f"Error in WebSocket receive: {str(e)}")  # Console log
    
    # Receive message from room group
    async def broadcast_frame(self, event):
        frame = event['frame']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'video_frame',
            'frame': frame
        }))
    
    # Handle viewer updates
    async def viewer_update(self, event):
        action = event['action']
        viewer_id = event['viewer_id']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'viewer_update',
            'action': action,
            'viewer_id': viewer_id
        }))