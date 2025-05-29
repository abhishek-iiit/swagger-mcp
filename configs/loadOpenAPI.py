from langchain_openai import AzureChatOpenAI
from langchain.tools import Tool
import requests

# 1. Setup your Azure OpenAI LLM
llm = AzureChatOpenAI(
    temperature=0.0,
    model="gpt-4o-mini",
    openai_api_key="abcdefghijklmnopqrstuvwxyz1234567890",
    azure_endpoint="https://ai-agent-tm-us-east-2.openai.azure.com",
    api_version="2023-09-01-preview",
    azure_deployment="ai-agent-4o"
)

# 2. Define a Tool for your MCP server
def mcp_tool_func(input_text: str) -> str:
    url = "http://localhost:3000/messages?sessionId=e257109d-5118-44b4-9f87-0bba6f965eba"
    payload = {"messages": [{"role": "user", "content": input_text}]}
    response = requests.post(url, json=payload)
    if response.ok:
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "No content returned.")
    else:
        return f"Error: {response.status_code} - {response.text}"

mcp_tool = Tool(
    name="MCP API Tool",
    func=mcp_tool_func,
    description="Use this tool to interact with the MCP server-backed API."
)

# 3. Setup LangChain Agent with the MCP tool
from langchain.agents import initialize_agent, AgentType

agent = initialize_agent(
    tools=[mcp_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 4. Example: Use the agent to make a request via the MCP tool
response = agent.run("Get a list of users from the API.")  # Adjust prompt as per your API
print(response)
