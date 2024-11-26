from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode
from state import State


class ToolNodeBuilder:
    """
    Builds a ToolNode.
    """

    def handle_error(self, state: State) -> dict:
        """
        Handles error

        Args:
            state (State): State

        Returns:
            dict: Dictionary of messages
        """
        error = state.get("error")
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f" Error: {repr(error)} \n Please fix the issue",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }

    def build(self, tools: list) -> dict:
        """
        Builds the ToolNode

        Args:
            tools (list): list of tools

        Returns:
            dict: Dictionary of tool node
        """
        return ToolNode(tools).with_fallbacks(
            [RunnableLambda(self.handle_error)], exception_key="error"
        )
