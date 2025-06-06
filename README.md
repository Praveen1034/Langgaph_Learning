# Langgraph Learning

Langgraph Learning is a comprehensive project demonstrating various agent-based chatbot architectures and graph-based learning workflows using Python. This repository is organized into multiple modules, each focusing on a different approach to conversational AI and graph-based computation.

## Project Structure

```
Chatbot_with_memory (agent_2)/
    Chatbot_memory.py
    README.md
Graph_Learning/
    Conditional_Graph.ipynb
    hello_world.ipynb
    image.png
    Looping_Graph.ipynb
    multi_input.ipynb
    pydantic_code.ipynb
    README.md
    Sequentail.ipynb
ReAct_Agent (Agent_3)/
    image.png
    ReAct.py
    README.md
Simple Bot (agent_1)/
    README.md
    Simple_Chatbot.py
```

## Modules Overview

### 1. Simple Bot (agent_1)
A basic chatbot implementation to demonstrate simple conversational logic. Useful as a starting point for understanding agent-based chatbots.

- **Simple_Chatbot.py**: Python script for a basic chatbot.
- **README.md**: Details and usage for this agent.

### 2. Chatbot with Memory (agent_2)
An advanced chatbot that maintains conversational memory, allowing for more context-aware interactions.

- **Chatbot_memory.py**: Implements a chatbot with memory features.
- **README.md**: Documentation for this agent.

### 3. ReAct Agent (Agent_3)
A chatbot agent using the ReAct (Reason + Act) paradigm, combining reasoning and action for more sophisticated responses.

- **ReAct.py**: Python script for the ReAct agent.
- **image.png**: Visual representation of the agent's workflow.
- **README.md**: Details and usage for this agent.

### 4. Graph Learning
A collection of Jupyter notebooks demonstrating graph-based learning, including sequential, conditional, and looping graphs, as well as multi-input and pydantic-based workflows.

- **hello_world.ipynb**: Introduction to graph learning.
- **Conditional_Graph.ipynb**: Conditional logic in graphs.
- **Looping_Graph.ipynb**: Looping constructs in graph workflows.
- **multi_input.ipynb**: Handling multiple inputs in graphs.
- **pydantic_code.ipynb**: Using Pydantic for data validation in graph workflows.
- **Sequentail.ipynb**: Sequential graph processing.
- **image.png**: Visual aid for graph learning.
- **README.md**: Documentation for graph learning notebooks.

## Getting Started

### Prerequisites
- Python 3.8+
- Jupyter Notebook (for running `.ipynb` files)
- Recommended: Create a virtual environment

### Installation
1. Clone the repository:
   ```powershell
   git clone https://github.com/Praveen1034/Langgaph_Learning.git
   cd Langgaph_Learning
   ```
2. (Optional) Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate
   ```
3. Install required packages:
   ```powershell
   pip install -r requirements.txt
   ```
   *(If a requirements.txt is not present, install packages as needed for each module.)*

### Running the Agents
- **Simple Bot:**
  ```powershell
  python "Simple Bot (agent_1)/Simple_Chatbot.py"
  ```
- **Chatbot with Memory:**
  ```powershell
  python "Chatbot_with_memory (agent_2)/Chatbot_memory.py"
  ```
- **ReAct Agent:**
  ```powershell
  python "ReAct_Agent (Agent_3)/ReAct.py"
  ```
- **Graph Learning Notebooks:**
  Open the desired notebook in Jupyter:
  ```powershell
  jupyter notebook
  ```

## Usage
Explore each module for specific instructions and examples. Each subfolder contains its own README with more details.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for review.

## License
This project is licensed under the MIT License.

## Acknowledgements
- Python community
- Jupyter Project
- OpenAI and LangChain for inspiration

---
For questions or support, please open an issue on GitHub.
