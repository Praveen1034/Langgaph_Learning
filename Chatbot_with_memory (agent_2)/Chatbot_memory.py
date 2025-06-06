from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

# Load environment variables from .env file 
load_dotenv("D:\\Langgraph\\.env")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",api_key = os.getenv("GEMINI_API_KEY")
)

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])
    
    state["messages"].append(AIMessage(content=response.content))
    print(f"AI Response: {response.content}")        
    return state

graph = StateGraph(AgentState)
# add node
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
graph = graph.compile()

conversational_history = []

user_input = input("Enter: ")
while user_input.lower() != "exit":
    conversational_history.append(HumanMessage(content=user_input))
    agent_state = {"messages": conversational_history}
    
    # Invoke the agent with the current state
    result = graph.invoke(agent_state)
    
    # Update the conversational history with the AI response
    conversational_history = result["messages"]
    
    user_input = input("Enter: ")