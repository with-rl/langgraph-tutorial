# Run a local server
# https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/
# langgraph cli commands: https://langchain-ai.github.io/langgraph/cloud/reference/cli/#commands
# 7. Test the API

from langgraph_sdk import get_client
import asyncio

client = get_client(url="http://localhost:2024")


async def main():
    async for chunk in client.runs.stream(
        None,  # Threadless run
        "agent",  # Name of assistant. Defined in langgraph.json.
        input={
            "messages": [
                {
                    "role": "human",
                    "content": "What is LangGraph?",
                }
            ],
        },
    ):
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")


asyncio.run(main())
