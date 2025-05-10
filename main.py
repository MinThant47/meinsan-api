from fastapi import FastAPI
import os
import requests
import time
import threading
from schema import chatbot
from langchain.schema import HumanMessage, AIMessage
from get_chathistory import save_chat_to_redis, load_chat_from_redis, clear_chat_from_redis

app = FastAPI()