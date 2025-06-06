from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import os

load_dotenv("D:\\Langgraph\\.env")

# Reducer Function
# Rule that control how update from node are combined with the existing state
# tells us how to merge the new data into the current state

# without a reducer, update would have replaced the existing value entirely

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]
    
@tool
def add(a : int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtracts the second number from the first."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers together."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divides the first number by the second."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b    

tools = [add, subtract, multiply, divide]

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",api_key = os.getenv("GEMINI_API_KEY")).bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content = 
                    "You are my AI assistant, please answer my query to the best of your ability")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> bool:
    """Check if the conversation should continue."""
    message = state["messages"]
    last_message = message[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)

# add node
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")

graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    }
)

graph.add_edge("tools", "our_agent")

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(f"Tool call: {message}")
        else:
            message.pretty_print()
    
inputs = {"messages": [("user", "What is 2 + 2? sub 3,4 and multi 5,6 and divide 8,8")]}
print_stream(app.stream(inputs, stream_mode="values"))