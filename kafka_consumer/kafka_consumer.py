import asyncio
import os
import json
from dotenv import load_dotenv
from shared.kafka_consumer import create_and_consume_messages
import websockets

load_dotenv()

DATABASE_SERVICE_URL = os.getenv("DATABASE_SERVICE_URL", "ws://database-service:8001")

# Define the mapping of topics to database service endpoints
endpoint_mapping = {
  "stock_data": f"{DATABASE_SERVICE_URL}/api/stock_data",
  "user_registrations": f"{DATABASE_SERVICE_URL}/api/user_registrations",
  "backtest_results": f"{DATABASE_SERVICE_URL}/backtest_results"
}

async def forward_message_to_service(topic, message):
  """
  Asynchronously forward the message to the corresponding WebSocket service endpoint.

  Args:
    topic (str): The topic name of the message.
    message (dict): The message content.
  """
  endpoint = endpoint_mapping.get(topic)

  if endpoint:
    try:
      message_json = json.dumps(message)
      async with websockets.connect(endpoint) as ws:
        await ws.send(message_json)
        # Optionally, you can receive a response
        # response = await ws.recv()
        # print(f"Received response: {response}")
      print(f"Successfully forwarded message to {endpoint}")
    except Exception as e:
      print(f"Failed to forward message to {endpoint}, Error: {e}")
  else:
    print(f"No endpoint defined for topic: {topic}")

async def consume_and_forward_messages(topic_names):
  """
  Asynchronously consumes messages from specified Kafka topics and forwards them to corresponding service endpoints.
  
  Args:
    topic_names (list): List of topic names to subscribe to.
  """
  for topic_name in topic_names:
    # Assuming create_and_consume_messages is adapted to be asynchronous or replaced with an async equivalent
    async for message in create_and_consume_messages(topic_name):
      await forward_message_to_service(topic_name, message)

# Example usage
async def main():
  topic_names = ['stock_data', 'user_registrations', 'backtest_results']
  await consume_and_forward_messages(topic_names)

if __name__ == "__main__":
  asyncio.run(main())