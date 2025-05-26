from upstash_redis import Redis
import json

#aungkyawkyawsoe
redis = Redis(url="https://wise-ladybug-34655.upstash.io", token="AYdfAAIjcDFlN2NlYTQwMTY4MmI0NWU4YTlkZjExOGE0YjEyYjcxOXAxMA")

from langchain.schema import HumanMessage, AIMessage

CHAT_KEY = "meisan"

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