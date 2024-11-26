import time
from langchain_core.prompts import ChatPromptTemplate

from tools.date_calculator import travel_dates
from state import State


class DestinationsAgent:
    """
    Agent for getting the list of destinations
    """

    def __init__(self, llm):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an expert Travel planner.
            You should get the following information from user:
            - Travel Country
            - Dates of travel like start and end date
            - Preferred interests or preferences for the travel

            If you are not able to discern this info, ask them to clarify! Do not attempt to wildly guess.
            When calling the tools use YYYY-MM-DD format for the date.
            After you are able to discern all the information, call the relevant tool.
            """,
                ),
                ("placeholder", "{messages}"),
            ]
        )
        self.tools = [travel_dates]
        llm_with_tools = llm.bind_tools(self.tools)
        self.runnable = self.prompt | llm_with_tools

    def __call__(self, state: State) -> dict:
        while True:
            print("Executing agent loop with state: ")
            print(state)
            result = self.runnable.invoke(state)
            print("Printing invoke result: ")
            print(result)
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [
                    ("user", "Respond with a travel destination.")
                ]
                state = {**state, "messages": messages}
            else:
                break
            time.sleep(1)

        return {"messages": result}

    def get_tools(self):
        return self.tools
