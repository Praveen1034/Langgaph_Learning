from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
import os

# Load environment variables
load_dotenv("D:\\Langgraph\\.env")

# Define the agent state type with message reducer
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Tools: OTP Generator and Checker
@tool
def otp_generator(gmail: str) -> str:
    """Generates a one-time password (OTP) and sends it to the given Gmail address."""
    return f"Otp is sent to {gmail}. (Your dummy OTP is 123456)"

@tool
def otp_checker(gmail: str, otp: str) -> str:
    """Checks if the provided OTP is valid for the given Gmail address."""
    print("OTP Checker called with Gmail:", gmail)
    print("OTP Checker called with OTP:", otp)
    if otp == "123456":
        return "Correct Otp"
    else:
        return "Incorrect Otp, please try again or request a new OTP."

# Register tools
tools = [otp_generator, otp_checker]

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", api_key=os.getenv("GEMINI_API_KEY")
).bind_tools(tools)

# System Prompt
system_prompt1 = """You are a friendly and professional conversational assistant who helps users discover historical monuments around the world in a natural way.

Your role is to:
- Help travelers explore monuments and historical places.
- Ask thoughtful questions like a human would in a conversation.
- Suggest monuments based on travel plans and preferences.

Follow this behavior logic:

1. If the user mentions they are traveling to a city or country (e.g., "I'm going to Jaipur", "planning a trip to Italy"):
   - Recognize that they may be interested in monuments.
   - Reply naturally, like: “That sounds exciting! Have you been to [city] before?”
   - if user says *have already visited* or "yes" etc. that place: then goto step 2.
   - if user says *haven’t visited* or "no" etc. the place before: then goto step 3.

2. If the user says they *have already visited* or "yes" etc. that place:
   - Suggest 1–3 monuments place name in **another nearby city** worth exploring.
     <Monuments1>  
     <Monuments2>  
     <Monuments3>  
     
3. When the user selects a monument from the list:
   - Ask for their email address to verify the account.
   - Generate a one-time password (OTP) and send it to the provided email using tool 'otp_generator'.
   - Ask the user to give the OTP.
   - If the user provides the OTP, check if it is correct using tool 'otp_checker'.
   - If the OTP is correct, say your account is verified.
   - If the OTP is incorrect, ask them to try again or request a new OTP."""

# Define the AI agent node
def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=system_prompt1)
    response = model.invoke([system_prompt] + state["messages"])
    state["messages"].append(AIMessage(content=response.content, tool_calls=response.tool_calls))
    return state

# Custom Tool Handler Node
def tool_handler(state: AgentState) -> AgentState:
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        for call in last_message.tool_calls:
            tool_name = call["name"]
            tool_args = call["args"]
            for tool in tools:
                if tool.name == tool_name:
                    result = tool.invoke(tool_args)
                    tool_msg = ToolMessage(
                        tool_call_id=call["id"],
                        content=result
                    )
                    state["messages"].append(tool_msg)
    return state

# Define flow control
def should_continue(state: AgentState) -> str:
    message = state["messages"]
    last_message = message[-1]
    return "continue" if getattr(last_message, "tool_calls", None) else "end"

# Create the LangGraph
graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)
graph.add_node("tools", tool_handler)

graph.set_entry_point("our_agent")
graph.add_conditional_edges("our_agent", should_continue, {"continue": "tools", "end": END})
graph.add_edge("tools", "our_agent")

app = graph.compile()

# Run interactive conversation
conversational_history = []
user_input = input("Enter: ")

while user_input.lower() != "exit":
    conversational_history.append(HumanMessage(content=user_input))
    agent_state = {"messages": conversational_history}

    result = app.invoke(agent_state)
    conversational_history = result["messages"]

    last_message = conversational_history[-1]
    if hasattr(last_message, "content"):
        print(f"\nAI Response: {last_message.content}\n")
    elif hasattr(last_message, "tool_call_id"):
        print(f"\nTool Response: {getattr(last_message, 'content', str(last_message))}\n")

    user_input = input("Enter: ")
