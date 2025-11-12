from upstash_redis import Redis
import json
from dotenv import load_dotenv
import os

load_dotenv()

#aungkyawkyawsoe
redis = Redis(url=os.getenv("REDIS_URL"), token=os.getenv("REDIS_TOKEN"))

from langchain_core.messages import HumanMessage, AIMessage

CHAT_KEY = os.getenv("REDIS_CHAT_KEY")

def save_chat_to_redis(chat_history):
    serializable = [
        {"type": type(m).__name__, "content": m.content}
        for m in chat_history
    ]
    redis.set(CHAT_KEY, json.dumps(serializable))

def load_chat_from_redis():
    data = redis.get(CHAT_KEY)
    if data:
        loaded = json.loads(data)
        history = []
        for msg in loaded:
            if msg["type"] == "HumanMessage":
                history.append(HumanMessage(content=msg["content"]))
            elif msg["type"] == "AIMessage":
                history.append(AIMessage(content=msg["content"]))
        return history
    return []

def clear_chat_from_redis():
    redis.delete(CHAT_KEY)