# Enhanced schema.py with multi-query support

from typing_extensions import TypedDict
from langgraph.graph import START, END, StateGraph
from node_func import (
    State, 
    # Multi-query functions
    split_questions, 
    inquiry_multiple, 
    process_multiple_queries,
    # Legacy single-query functions (for backward compatibility)
    inquiry, 
    FAQ, 
    EC_info, 
    McE_info, 
    CMD, 
    Recommender, 
    Navigator, 
    not_found, 
    route_app
)

# Create the enhanced workflow with multi-query support
workflow = StateGraph(State)

# Add nodes for multi-query processing
workflow.add_node("split_questions", split_questions)
workflow.add_node("inquiry_multiple", inquiry_multiple)
workflow.add_node("process_multiple", process_multiple_queries)

# Add legacy nodes (kept for backward compatibility)
workflow.add_node("inquiry", inquiry)
workflow.add_node("FAQ", FAQ)
workflow.add_node("EC_info", EC_info)
workflow.add_node("McE_info", McE_info)
workflow.add_node("Recommender", Recommender)
workflow.add_node("Navigator", Navigator)
workflow.add_node("CMD", CMD)
workflow.add_node("not_found", not_found)

# Define the main workflow
workflow.add_edge(START, "split_questions")
workflow.add_edge("split_questions", "inquiry_multiple")
workflow.add_edge("inquiry_multiple", "process_multiple")
workflow.add_edge("process_multiple", END)

# Compile the chatbot
chatbot = workflow.compile()