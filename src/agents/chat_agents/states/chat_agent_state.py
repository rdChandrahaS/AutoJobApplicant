from typing_extensions import TypedDict, Annotated
from langchain.messages import AnyMessage
import operator

class ChatAgentState(TypedDict):
    """
    """
    messages: Annotated[list[AnyMessage], operator.add]

