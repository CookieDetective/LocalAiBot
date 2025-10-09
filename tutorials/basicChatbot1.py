from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langchain.chat_models import init_chat_model

from IPython.display import Image, display

import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = init_chat_model(model="gpt-3.5-turbo")
#Wheen defining a graph, the first stewp is to define its state. The State includes the graph's schema and reducer functions that handle state updates.
#The below State is a schema with one key: messages. The reducer function is used to append messages to the list instead of overwriting it. Keys without a reducer annotation overwrite previous values
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.

#Add a chatbot node, node represent units fo work and are typically regular functions
graph_builder.add_node("chatbot", chatbot)
#Add an entry point to tell the graph where to start its work each time it is run
graph_builder.add_edge(START, "chatbot")
#Add an exit point to indicate where the graph should finish execution. This will be helpful for more complex flows
graph_builder.add_edge("chatbot", END)

#Before running the graph we will need to compile it. We use compile() on the graph builder which creates a CompiledGraph we can invoke on our state
graph = graph_builder.compile()
#This is meant to display the graph as a visual but it has not been coming up. Will be implemented at a later date
#try:
#    display(Image(graph.get_graph().draw_mermaid_png()))
#except Exception:
#    # This requires some extra dependencies and is optional
#    pass

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        stream_graph_updates(user_input)
        #display(Image(graph.get_graph().draw_mermaid_png()))
    except:
        # fallback if input() is not available
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break