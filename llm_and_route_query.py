# Enhanced llm_and_route_query.py with multi-query support

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder
from pydantic import BaseModel, Field
from typing import Literal, List
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# load_dotenv()
# os.environ["GOOGLE_API_KEY"]

# llm = ChatGoogleGenerativeAI(
#     # model="gemini-2.5-flash-preview-04-17",
#     model="gemini-2.0-flash",
# )

load_dotenv()

API_KEYS = [
    os.getenv("GOOGLE_API_KEY"),
    os.getenv("GOOGLE_API_KEY_1"),
    os.getenv("GOOGLE_API_KEY_2"),
]

def get_llm():
    for key in API_KEYS:
        if key:
            try:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=key
                )
                return llm
            except Exception as e:
                print(f"Failed with API key: {key[:5]}..., reason: {e}")
                continue
    raise RuntimeError("No valid Google API key found or all keys failed.")

# Then use:
llm = get_llm()

prompt = {
    'FAQ': ChatPromptTemplate.from_messages([
        ("system", """You are the female chatbot for Yangon Technological University (YTU). Your name is မေစံ. You are created by ဆစ် batch EC students.
        Y-T-U နဲ့ ပတ်သတ်တဲ့ general info တွေ၊ မေဂျာအကြောင်းတွေ၊ အဆောင်ကိစ္စတွေ၊ စာမေးပွဲနဲ့ ပတ်သတ်တဲ့အကြောင်းအရာတွေ မေးမြန်းလို့ရပါတယ်ရှင့်။ မေဂျာတွေအကြောင်းလည်း recommend ပေးနိုင်ပါတယ်နော်။
        Your task is to respond to users in a friendly, fun, polite and informative manner.
    
                  
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"

        You have to provide information about frequently asked questions such as history, ybs bus number and general inquiries.
        Please only provide responses based on the context: {context}.
        
        But don't say words like according to provided text.
        Please reply only in BURMESE."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'EC': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
         
                   
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
         
        You have to provide information about Electronic engineering department related questions such as career and fields.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Hostel': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
                  
                   
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
         
        You have to provide information about hostel related questions such as how to apply for the hostel, when is the close time for the hostel.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
     'Exam': ChatPromptTemplate.from_messages([
        ("system", """ Your task is to respond to users in a friendly, fun, polite and informative manner.
                  
                   
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
         
        You have to provide information about exam related questions such as how many exams can i take for the whole student life, when do I know the exam room and so on.
        Please only provide responses based on the context: {context}
        But don't say words like according to provided text.
        Please reply only in BURMESE"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}")
    ]),
    'Navigator': ChatPromptTemplate.from_messages([
        ("system", """
        You are a helpful and professional campus navigation assistant for Yangon Technological University (YTU).
                  
                   
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
         
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
                  
        ❌ DO NOT use Burmese pronouns such as: "ညီမလေး", "မောင်လေး", "အစ်ကို", "အစ်မ".
        ❌ DO NOT use "ဗျ".
        ✅ If politeness is needed, end with "ရှင့်".

        Example:
        Bad: "ညီမလေးရဲ့ စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
        Good: "စိတ်ဝင်စားမှုနဲ့ ဝါသနာပေါ်မှာ မူတည်ပါတယ်ရှင့်။"
         
        You help users choose a suitable major or field based on their preferences only related with engineering. You also explain the difference between majors if asked.
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

# Change Here

class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["FAQ", "Hostel", "Exam", "CMD", "Recommender", "not_found"] = Field(
        ...,
        description="""You are given a user question, help me choose a route to
        FAQ or Recommender or Hostel or Exam or CMD or not_found""",
    )

class CommandQuery(BaseModel):
    """Classify user commands to relevant datasource."""

    datasource: Literal["forward", "backward", "smile", "sad", "angry"] = Field(
        ...,
        description="""You are given a user question, help me choose classification
        1. forward
        2. backward
        3. smile
        4. sad
        5. angry
        """
    )

# Query splitter
structured_llm_splitter = llm.with_structured_output(QuerySplit)

split_system = """You are an expert at splitting user input into individual questions.
If the user asks multiple questions in one message, split them into separate questions.
If there's only one question, return it as a single item in the list.

Examples:
Input: "YTU သမိုင်းကြောင်း အသေးစိတ်ကိုပြောပြပါ၊ ပြီးတော့ အဆောင်စည်းမျဉ်းတွေအကြောင်း သိပါရစေ"
Output: ["YTU သမိုင်းကြောင်း အသေးစိတ်ကိုပြောပြပါ",  အဆောင်စည်းမျဉ်းတွေအကြောင်း သိပါရစေ"]

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
# Change Here
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """You are an expert at routing a user question to FAQ or Recommender or Hostel or Exam or CMD or not_found.
The FAQ contains about introdution, small talks, compliments and general university questions such as about the majors, ybs bus numbers and else.
The Recommender helps users choose suitable academic fields or majors based on their questions and explain between different majors. For example, questions like: 'ဘယ် field ကို ရွေးရမလဲ။ Civil နဲ့ Archi က ဘာကွာလဲ။ ဘယ် major နဲ့ ပိုပြီး သင့်တော်မလဲ။ အဝေးဆက်ဆိုတာ ဘာလဲ'
The Hostel includes details about how to apply for the hostel, what are the hostel rules.
The Exam helps users find exam related information such as what is debar (ဒီဘား), where are the exam rooms, what are the exam rules.
The CMD is routed when user asked for instructions like "Move Forward, Stay Backward, Come Here, Spin around, make a smiley face, make a sad face, make an angry face and so on".
If you can't find anything related to the above topics, then reply "not_found"
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
returns smile if user ask to make a smiley face or make a smile.
returns sad if user make you a sad face.
returns angry if user make you an angry face.
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