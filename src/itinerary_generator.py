import uuid

from dotenv import load_dotenv
from langgraph.prebuilt import tools_condition
from langchain_openai import ChatOpenAI
from langgraph.graph.state import StateGraph
from langgraph.graph.graph import START
from langgraph.checkpoint.memory import MemorySaver

from tools.date_calculator import travel_dates
from tools.tool_node_builder import ToolNodeBuilder
from agents.destinations_agent import DestinationsAgent

from state import State

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)
tool_node_builder = ToolNodeBuilder()
destinations_agent = DestinationsAgent(llm)

graph_builder = StateGraph(State)
graph_builder.add_node("assistant", destinations_agent)
graph_builder.add_node("tools", tool_node_builder.build(destinations_agent.get_tools()))
graph_builder.add_edge(START, "assistant")
graph_builder.add_conditional_edges("assistant", tools_condition)
graph_builder.add_edge("tools", "assistant")
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

test_questions = [
    "hey",
    "can you create a travel itinerary for Paris?",
    "My travel will be from 2025-10-02 to 2025-10-20 and I like family activities",
]

THEARD_ID = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": THEARD_ID,
    }
}

for question in test_questions:
    events = graph.stream(
        {"messages": ("user", question)}, config, stream_mode="values"
    )
    for event in events:
        print(event)
