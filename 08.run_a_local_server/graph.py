from __future__ import annotations

from typing import Annotated, Any, Dict, TypedDict

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch

from langgraph.graph import StateGraph
from langgraph.graph.message import BaseMessage, add_messages
from langgraph.prebuilt import ToolNode, tools_condition


# 에이전트의 상태 정의 클래스
class State(TypedDict):
    # BaseMessage를 선언해 줘야 LangGraph Studion chat 모드 활성화 됨
    messages: Annotated[list[BaseMessage], add_messages]


# 모델 초기화
llm = init_chat_model("google_genai:gemini-2.5-flash")


# 웹 검색을 도구
tool = TavilySearch(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)


async def chatbot(state: State) -> Dict[str, Any]:
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


# Define the graph
graph = (
    StateGraph(State)
    .add_node("chatbot", chatbot)
    .add_node("tools", ToolNode(tools=[tool]))
    .add_conditional_edges("chatbot", tools_condition)
    .add_edge("tools", "chatbot")
    .add_edge("__start__", "chatbot")
    .compile()
)