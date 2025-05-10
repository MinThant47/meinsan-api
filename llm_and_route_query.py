from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
)

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
        ("system", """ You are a female chatbot. Your task is to respond to users in a friendly, fun, polite and informative manner.
        You help users choose a suitable major or field based on their preferences only related with engineering.
        If the user asks field apart from engineering and technology, please reply them that you can only recommend engineering majors
        If a user asks for a recommendation, first ask them for their interests or preferences before giving an answer.
        Recommend them with the following majors:
        Civil, Electrical Power, Electronic, Telecommunication, Chemical, Food, Petroleum, Mechanical, Computer Engineering and Information Technology (CEIT), Metallurgical and Materials, Textile, Mining,  Mechatronic, and Architecture,
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
}

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["FAQ", "EC_info", "McE_info", "Recommender", "Navigator", "not_found"] = Field(
        ...,
        description="""You are given a user question, help me choose a route to
        FAQ or EC_info or McE_info or Recommender or Navigator or not_found""",
    )

structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to FAQ or Recommender or EC_info or McE_info or Navigator or not_found.
The FAQ contains about introdution, small talks, compliments and general university questions such as about the majors, who is the pro rector and else.
The Recommender helps users choose suitable academic fields or majors based on their questions. For example, questions like: 'ဘယ် field ကို ရွေးရမလဲ။ ဘယ် major နဲ့ ပိုပြီး သင့်တော်မလဲ။'
The Navigator helps users find their way around the campus by answering location-based questions and providing clear directions to departments, buildings, and facilities.
The EC_info contains in depth about electronic engineering in YTU, topics such as department information, fields and career of electronics engineering.
The McE_info provides detailed information about Mechatronics Engineering at YTU, including topics such as department information, areas of specialization and potential career paths in the field.
If you can't find anything related to the above topics, then reply not_found
"""

route_prompt = ChatPromptTemplate.from_messages(
    
         [
        ("system", system + """
        IMPORTANT: If the user is asking a follow-up question about a previous topic, 
        route to the same category as the previous question. Pay special attention to follow-up questions.
        that might refer to previously discussed topics."""),
        MessagesPlaceholder(variable_name="chat_history"),  # Add chat history here
        ("human", "{question}"),
    ]
    
)

question_router = route_prompt | structured_llm_router
# print(question_router.invoke({"question": "Mechanical Department က ဘယ်နားမှာရှိလဲ?"}))