from fastapi import FastAPI, WebSocket
from sqlalchemy.orm import Session
from database_models import User, StockPrice # ... other relevant models
from src.utils.kafka_utils.consumer import consume_from_kafka
import json
import logging

app = FastAPI()


@app.websocket("/ws/data")  # WebSocket endpoint
async def websocket_endpoint(websocket: WebSocket):
    """Receives data from Kafka consumer and inserts it into the database."""
    await websocket.accept()
    
    # Message Type Handler Mapping
    message_handlers = {
        "user_registrations": handle_user_registration,
        "stock_data": handle_stock_data,
        "backtest_results": handle_backtest_results,
        # Add more handlers for other message types if needed
    }

    try:
        for message in consume_from_kafka(consumer, "stock_data"):
            logger.info(f"Received message from kafka: {message}")
            await websocket.send_json({"message": "Stock data saved to database"})

        for message in consume_from_kafka(consumer, "user_registrations"):
            await websocket.send_json(message)

        for message in consume_from_kafka(consumer, "backtest_results"):
            await websocket.send_json(message)


    except websockets.WebSocketException as e:
        logger.error(f"WebSocket Error: {e}")
    finally:
        await websocket.close()
    
def handle_user_registration(data: dict, db: Session):
    """Handles user registration data from Kafka."""
    try:
        # Validate user data (e.g., check for required fields)
        # ...

        # Hash the password (ensure you have a password hashing mechanism)
        hashed_password = hash_password(data["password"])
        data.pop('password') # Remove the plain text password

        # Create and save the user to the database using your models
        new_user = User(**data, password=hashed_password)
        db.add(new_user)
        db.commit()

    except Exception as e:  # Catch more specific exceptions as needed
        logger.error(f"Error processing user registration: {e}")
        # Consider sending an error message back to the client
def handle_stock_data(data: dict, db: Session):
    """Handles stock data from Kafka."""
    try:
        # Validate and process stock data
        # ...
        
        # Insert or update data in Fact_StockPrices using SQLAlchemy
        # ...

    except Exception as e:
        logger.error(f"Error processing stock data: {e}")

def handle_backtest_results(data: dict, db: Session):
    """Handles backtest results from Kafka."""
    try:
        # Validate and process backtest results
        # ...

        # Insert data in Fact_Backtests using SQLAlchemy
        # ...

    except Exception as e:
        logger.error(f"Error processing backtest results: {e}")
