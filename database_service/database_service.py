from fastapi import FastAPI, WebSocket
from sqlalchemy.orm import Session
from database_models import Dim_Users, Fact_StockPrices
import json
import logging
import coloredlogs
from starlette.websockets import WebSocketState

app = FastAPI()


coloredlogs.install()  # install a handler on the root logger

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level="INFO",
    format="%(levelname)s - %(message)s",
    # format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger.info("Database Service started")

@app.websocket("/ws/user_registrations")
async def websocket_user_registrations(websocket: WebSocket):
    """WebSocket endpoint to receive and process user registration data."""
    await websocket.accept()
    try:
        async for message_str in websocket.iter_text():
            message = json.loads(message_str)
            logger.info(f"Received user registration data: {message}")
            try:
                # Insert user registration data into the database
                print(message)
            except Exception as e:  
                logger.error(f"Error processing user registration: {e}")
    finally:
        if not websocket.client_state == WebSocketState.DISCONNECTED:
            await websocket.close()



