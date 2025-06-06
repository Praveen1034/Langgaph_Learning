from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv
import os

# Load environment variables from .env file 
load_dotenv("D:\\Langgraph\\.env")

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",api_key = os.getenv("GEMINI_API_KEY")
)

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"Response: {response.content}")
    return state

# Define the graph
graph = StateGraph(AgentState)

# add node
graph.add_node("process", process)

graph.add_edge(START, "process")
graph.add_edge("process", END)

agent = graph.compile()


user_input = input("Enter: ")
while user_input.lower() != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
    
    
    
    