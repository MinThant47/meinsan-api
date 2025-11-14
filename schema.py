# Enhanced schema.py with multi-query support

from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from node_func import (
    State, 
    split_questions, 
    inquiry_multiple, 
    process_multiple_queries,
)

# Create the enhanced workflow with multi-query support
workflow = StateGraph(State)

# Add nodes for multi-query processing
workflow.add_node("split_questions", split_questions)
workflow.add_node("inquiry_multiple", inquiry_multiple)
workflow.add_node("process_multiple", process_multiple_queries)

# Define the main workflow
workflow.add_edge(START, "split_questions")
workflow.add_edge("split_questions", "inquiry_multiple")
workflow.add_edge("inquiry_multiple", "process_multiple")
workflow.add_edge("process_multiple", END)

# Compile the chatbot
chatbot = workflow.compile()