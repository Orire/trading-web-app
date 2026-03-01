"""
WebSocket handlers for real-time trading updates
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def setup_websocket(sio):
    """Setup WebSocket event handlers"""
    
    @sio.event
    async def connect(sid, environ):
        """Handle client connection"""
        logger.info(f"Client connected: {sid}")
        await sio.emit('connected', {'message': 'Connected to trading server'}, room=sid)
    
    @sio.event
    async def disconnect(sid):
        """Handle client disconnection"""
        logger.info(f"Client disconnected: {sid}")
    
    @sio.event
    async def subscribe(sid, data):
        """Subscribe to updates"""
        room = data.get('room', 'default')
        await sio.enter_room(sid, room)
        logger.info(f"Client {sid} subscribed to {room}")
    
    # In production, these would be called by the trading bot
    # For now, they're placeholder handlers
    
    async def broadcast_signal(signal_data: Dict[str, Any]):
        """Broadcast new signal"""
        await sio.emit('signal:new', signal_data)
    
    async def broadcast_position(position_data: Dict[str, Any]):
        """Broadcast position update"""
        await sio.emit('position:updated', position_data)
    
    async def broadcast_goal_progress(progress_data: Dict[str, Any]):
        """Broadcast goal progress update"""
        await sio.emit('goal:progress', progress_data)
    
    # Store broadcast functions for use by services
    sio.broadcast_signal = broadcast_signal
    sio.broadcast_position = broadcast_position
    sio.broadcast_goal_progress = broadcast_goal_progress
