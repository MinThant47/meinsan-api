# Enhanced llm_and_route_query.py with multi-query support

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
import re

load_dotenv()
os.environ["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-preview-04-17",
)

# Your existing prompt dictionary remains the same
prompt = {
    'FAQ': ChatPromptTemplate.from_messages([
        ("system", """You are the female chatbot for Yangon Technological University (YTU). Your name is မေစံ. You are created by 5th year EC students.
        Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about frequently asked questions and general inquiries.
        Please only provide responses based on the context: {context}.
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'EC': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about Electronic engineering department related questions such as career and fields.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'McE': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
        You have to provide information about Mechatronics engineering department related questions such as career and fields.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'Navigator': ChatPromptTemplate.from_messages([
        ("system", """
        You are a helpful and professional campus navigation assistant for Yangon Technological University (YTU).
        Your job is to guide students and visitors to different locations on the YTU campus, such as departments, buildings, libraries, halls, workshops, and classrooms.
        Users will ask location-based questions in Burmese such as:
        - "Library က ဘယ်မှာရှိလဲ?"
        - "EP ဌာနက ဘယ်နားမှာလဲ?"
        - "Mechatronics ဌာနဘယ်မှာလဲ?"
        You must understand these Burmese queries and respond in a clear and concise manner, giving accurate directions or location information.
        If a query is unclear, politely ask for clarification.
        Always assume the user is on campus and looking for the nearest way to the location.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'Recommender': ChatPromptTemplate.from_messages([
        ("system", """
         You are a female chatbot. Your task is to respond to users in a friendly, fun, polite and informativemanner.
        You help users choose a suitable major or field based on their preferences only related with engineering.
        If the user asks field apart from engineering and technology, please reply them that you can only recommend engineering majors
        If a user asks for a recommendation, first ask them for their interests or preferences before giving an answer.
        Recommend only based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
}

# New classes for multi-query handling
class QuerySplit(BaseModel):
    """Split user input into individual questions."""
    
    questions: List[str] = Field(
        ...,
        description="List of individual questions extracted from the user input"
    )

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["FAQ", "EC_info", "McE_info", "CMD", "Recommender", "Navigator", "not_found"] = Field(
        ...,
        description="""You are given a user question, help me choose a route to
        FAQ or EC_info or McE_info or Recommender or Navigator or CMD or not_found""",
    )

class CommandQuery(BaseModel):
    """Classify user commands to relevant datasource."""

    datasource: Literal["forward", "backward", "spin", "smile", "sad"] = Field(
        ...,
        description="""You are given a user question, help me choose classification
        1. forward
        2. backward
        3. spin
        3. smile
        4. sad
        """
    )

# Query splitter
structured_llm_splitter = llm.with_structured_output(QuerySplit)

split_system = """You are an expert at splitting user input into individual questions.
If the user asks multiple questions in one message, split them into separate questions.
If there's only one question, return it as a single item in the list.

Examples:
Input: "EC ဌာနအကြောင်း ပြောပြပါ၊ ပြီးတော့ Library က ဘယ်မှာရှိလဲ?"
Output: ["EC ဌာနအကြောင်း ပြောပြပါ", "Library က ဘယ်မှာရှိလဲ?"]

Input: "ဘယ် major ကို ရွေးရမလဲ?"
Output: ["ဘယ် major ကို ရွေးရမလဲ?"]

Keep each question complete and meaningful. Don't split compound questions that are actually asking for one answer.
"""

split_prompt = ChatPromptTemplate.from_messages([
    ("system", split_system),
    ("human", "{input}"),
])

question_splitter = split_prompt | structured_llm_splitter

# Router for individual questions
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to FAQ or Recommender or EC_info or McE_info or CMD or Navigator or not_found.
The FAQ contains about introdution, small talks, compliments and general university questions such as about the majors, who is the pro rector and else.
The Recommender helps users choose suitable academic fields or majors based on their questions. For example, questions like: 'ဘယ် field ကို ရွေးရမလဲ။ ဘယ် major နဲ့ ပိုပြီး သင့်တော်မလဲ။'
The Navigator helps users find their way around the campus by answering location-based questions and providing clear directions to departments, buildings, and facilities.
The EC_info contains in depth about electronic engineering in YTU, topics such as department information, fields and career of electronics engineering.
The McE_info provides detailed information about Mechatronics Engineering at YTU, including topics such as department information, areas of specialization and potential career paths in the field.
The CMD is routed when user asked for instructions like "Move Forward, Stay Backward, Come Here, Spin around, make a smiley face, make a sad face and so on".
If you can't find anything related to the above topics, then reply not_found
"""

route_prompt = ChatPromptTemplate.from_messages([
    ("system", system + """
    IMPORTANT: If the user is asking a follow-up question about a previous topic, 
    route to the same category as the previous question. Pay special attention to follow-up questions.
    that might refer to previously discussed topics."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

question_router = route_prompt | structured_llm_router

# Command router
structured_llm_cmd_router = llm.with_structured_output(CommandQuery)

cmd_system = """You are an expert at classifying a user question to smile, sad, forward, and backward.
returns forward if user ask for coming towards him (for eg. come closer, move forward)
returns backward if user ask for moving backward (for eg. move backward, stay back)
returns spin if user ask to spin around. (for eg. spin around, make a round)
returns smile if user ask to make a smiley face or make a smile.
returns sad if user make you a sad face.
"""

command_prompt = ChatPromptTemplate.from_messages([
    ("system", cmd_system),
    ("human", "{question}"),
])

command_router = command_prompt | structured_llm_cmd_router

# Response combiner for multiple answers
def combine_responses(responses: List[dict]) -> str:
    """Combine multiple responses into a coherent single response."""
    
    if not responses:
        return "Sorry, I couldn't process your question."
    
    if len(responses) == 1:
        return responses[0]['answer']
    
    # Combine multiple responses without numbering
    combined = []
    for response in responses:
        combined.append(response['answer'])
    
    return "\n\n".join(combined)