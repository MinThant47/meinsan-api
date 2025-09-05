# Enhanced node_func.py with multi-query support

from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, BaseMessage
from llm_and_route_query import llm, question_router, command_router, prompt, question_splitter, combine_responses
from typing_extensions import TypedDict, List
from load import get_context

class State(TypedDict):
    question: str
    questions: List[str]  # New field for split questions
    topics: List[str]     # New field for multiple topics
    topic: str
    command: str
    responses: List[dict] # New field for multiple responses
    response: str
    chat_history: List[BaseMessage]

def split_questions(state: State) -> State:
    """Split the input into individual questions if multiple queries exist."""
    question = state["question"]
    
    try:
        split_result = question_splitter.invoke({"input": question})
        questions = split_result.questions
        
        print(f"---SPLIT INPUT INTO {len(questions)} QUESTIONS---")
        for i, q in enumerate(questions, 1):
            print(f"Question {i}: {q}")
            
        return {"questions": questions}
    except Exception as e:
        print(f"Error splitting questions: {e}")
        # Fallback: treat as single question
        return {"questions": [question]}

def inquiry_multiple(state: State) -> State:
    """Route multiple questions to their respective topics."""
    questions = state.get("questions", [state["question"]])
    chat_history = state.get("chat_history", [])
    
    topics = []
    
    for question in questions:
        try:
            source = question_router.invoke({"question": question, "chat_history": chat_history})
            topics.append(source.datasource)
            print(f"---ROUTE QUESTION '{question[:50]}...' TO {source.datasource}---")
        except Exception as e:
            print(f"Error routing question '{question}': {e}")
            topics.append("not_found")
    
    return {"topics": topics}

def process_multiple_queries(state: State) -> State:
    """Process all questions and generate responses."""
    questions = state.get("questions", [])
    topics = state.get("topics", [])
    chat_history = state.get("chat_history", [])
    
    responses = []
    commands = []
    
    # Process each question-topic pair
    for question, topic in zip(questions, topics):
        try:
            if topic == "FAQ":
                response = get_context("YTUFAQ", question, prompt['FAQ'], chat_history)
                responses.append(response)
                commands.append("stop")
                
            # elif topic == "EC_info":
            #     response = get_context("YTUEC", question, prompt['EC'], chat_history)
            #     responses.append(response)
            #     commands.append("stop")
                
            elif topic == "Hostel":
                response = get_context("YTUHostel", question, prompt['Hostel'], chat_history)
                responses.append(response)
                commands.append("stop")

            elif topic == "Exam":
                response = get_context("YTUExam", question, prompt['Exam'], chat_history)
                responses.append(response)
                commands.append("stop")    
                
            # elif topic == "Navigator":
            #     response = get_context("YTUMap", question, prompt['Navigator'], chat_history)
            #     responses.append(response)
            #     commands.append("stop")
                
            elif topic == "Recommender":
                response = get_context("YTUMajors", question, prompt['Recommender'], chat_history)
                responses.append(response)
                commands.append("stop")
                
            elif topic == "CMD":
                question_msg = HumanMessage(content=question)
                system_message = SystemMessage(content="You are a fun physical robot who responds with sound actively when you ask me to move closer or step back or spin around. You can be also requested to smile or show a sad face or an angry face! Please Reply Only in Burmese!")
                
                # response = {"input": question_msg, "answer": llm.invoke([system_message, question_msg]).content}
                
                classifier = command_router.invoke({"question": question_msg})
                
                if(classifier.datasource == "forward"):
                    response = {"input": question_msg, "answer": "လာနေပြီ ဘေးကို ဘေးကို ဝှီး ဝှီး"}
                elif(classifier.datasource == "backward"):
                    response = {"input": question_msg, "answer": "ဟိတ် နောက်ဆုတ်လာပြီနော် တီ တီ"}
                elif(classifier.datasource == "smile"):
                    response = {"input": question_msg, "answer": "ဟီး ဟီး"}
                elif(classifier.datasource == "sad"):
                    response = {"input": question_msg, "answer": "မေးတာတွေများတော့ စိတ်ညစ်လာပြီ"}
                elif(classifier.datasource == "angry"):
                    response = {"input": question_msg, "answer": "ဘာမှ လာမမေးနဲ့ ဒါပဲ ဟွန့်"}

                responses.append(response)
                commands.append(classifier.datasource)
                
            else:  # not_found
                question_msg = HumanMessage(content=question + "မေးတဲ့ မေးခွန်းက ပေးထားတဲ့ အချက်အလက်တွေမှာမပါလို့ အသေးစိတ်သိချင်ရင် ကျောင်းသားရေးရာမှာ မေးမြန်းနိုင်ပါတယ်။")
                system_message = SystemMessage(content="တောင်းပန်ပါတယ်ရှင့်။ မေစံက YTU နဲ့ ပတ်သတ်တဲ့ အချက်အလက်တွေကိုပဲ ဖြေပေးနိုင်ပါတယ်ရှင့်")
                
                response = {"input": question_msg, "answer": llm.invoke([system_message, question_msg]).content}
                responses.append(response)
                commands.append("stop")
                
        except Exception as e:
            print(f"Error processing question '{question}': {e}")
            # Fallback response
            fallback_response = {
                "input": HumanMessage(content=question),
                'answer': "ဒီမေးခွန်းနဲ့ပတ်သက်ပြီး အသေးစိတ် အချက်အလက် မသေချာသေးတာကြောင့် ကျောင်းသားရေးရာ သို့မဟုတ် သင်တန်းရေးရာကို ဆက်သွယ်ပြီး မေးမြန်းနိုင်ပါတယ်။"
            }
            responses.append(fallback_response)
            commands.append("stop")
    
    # Combine responses
    combined_answer = combine_responses(responses)
    
    # Determine primary command (prioritize non-stop commands)
    primary_command = "stop"
    for cmd in commands:
        if cmd != "stop":
            primary_command = cmd
            break
    
    final_response = {
        "input": state["question"],
        "answer": combined_answer
    }
    
    return {
        "responses": responses,
        "response": final_response,
        "command": primary_command
    }

# # Legacy single-query functions (kept for compatibility)
# def inquiry(state: State) -> State:
#     question = state["question"]
#     source = question_router.invoke({"question": question, "chat_history": state["chat_history"]})

#     if source.datasource == "FAQ":
#         print("---ROUTE QUESTION TO FAQ---")
#         return {"topic": "FAQ"}
#     elif source.datasource == "EC_info":
#         print("---ROUTE QUESTION TO EC---")
#         return {"topic": "EC_info"}
#     elif source.datasource == "McE_info":
#         print("---ROUTE QUESTION TO McE---")
#         return {"topic": "McE_info"}
#     elif source.datasource == "Recommender":
#         print("---ROUTE QUESTION TO Recommender---")
#         return {"topic": "Recommender"}
#     elif source.datasource == "Navigator":
#         print("---ROUTE QUESTION TO Navigator---")
#         return {"topic": "Navigator"}
#     elif source.datasource == "CMD":
#         print("---ROUTE QUESTION TO Command---")
#         return {"topic": "CMD"}
#     else:
#         print("Can't find related documents")
#         return {"topic": "not_found"}

# def FAQ(state: State) -> State:
#     print("Routing to FAQ : ")
#     question = state["question"]
#     response = get_context("YTUFAQ", question, prompt['FAQ'], state["chat_history"])
#     return {"response": response, "command": "stop"}

# def EC_info(state: State) -> State:
#     print("Routing to EC Information : ")
#     question = state["question"]
#     response = get_context("YTUEC", question, prompt['EC'], state["chat_history"])
#     return {"response": response, "command": "stop"}

# def McE_info(state: State) -> State:
#     print("Routing to McE Information : ")
#     question = state["question"]
#     response = get_context("YTUMCE", question, prompt['McE'], state["chat_history"])
#     return {"response": response, "command": "stop"}

# def Navigator(state: State) -> State:
#     print("Routing to Navigator : ")
#     question = state["question"]
#     response = get_context("YTUMap", question, prompt['Navigator'], state["chat_history"])
#     return {"response": response, "command": "stop"}

# def Recommender(state: State) -> State:
#     print("Routing to Recommender : ")
#     question = state["question"]
#     response = get_context("YTUMajors", question, prompt['Recommender'], state["chat_history"])
#     return {"response": response, "command": "stop"}

# def CMD(state):
#     print("---Command Instruction---")
#     question = HumanMessage(content=state["question"])
#     system_message = SystemMessage(content="You are a fun physical robot who responds with sound actively when you ask me to move closer or step back or spin around. You can be also requested to smile or show a sad face! Please Reply Only in Burmese!")

#     response = {"input": question, "answer": llm.invoke([system_message, question]).content}
#     classifier = command_router.invoke({"question": question})
    
#     return {"response": response, "command": classifier.datasource}

# def not_found(state: State) -> State:
#     print("Not Found: Out of scope")
#     question = HumanMessage(content=state["question"] + "The answer to the question isn't available in the document.")
#     system_message = SystemMessage(content="You provides polite and concise reponse when there is no relevant information in the given documents in burmese.")

#     response = {"input": question, "answer": llm.invoke([system_message, question]).content}
#     return {"response": response, "command": "stop"}

# def route_app(state: State) -> str:
#     if state["topic"] == "FAQ":
#         return "FAQ"
#     elif state["topic"] == "EC_info":
#         return "EC_info"
#     elif state["topic"] == "McE_info":
#         return "McE_info"
#     elif state["topic"] == "Recommender":
#         return "Recommender"
#     elif state["topic"] == "Navigator":
#         return "Navigator"
#     elif state["topic"] == "CMD":
#         return "CMD"
#     elif state["topic"] == "not_found":
#         return "not_found"