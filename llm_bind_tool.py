from llm import llm
from tools.commit_detail_tool import get_recent_commits
from tools.open_issue_detail_tool import get_open_issues
from tools.repo_detail_tool import get_repository_details

from langchain_core.messages import HumanMessage, ToolMessage

tools = [
    get_repository_details,
    get_recent_commits,
    get_open_issues,
]

llm_with_tools = llm.bind_tools(tools)

response = llm_with_tools.invoke("Show recent commits for rongmingsun/langgraph-dynamic-supervisor")
print("Text:", response.content)
print("Requested tools:", response.tool_calls)
print(response)



query = HumanMessage("Show recent commits for rongmingsun/langgraph-dynamic-supervisor")
messages = [query]
responses = llm_with_tools.invoke(messages)

messages.append(responses)

# 3. Map tool names to their executable objects.
tools_by_name = {tool.name: tool for tool in tools}

# 4. Execute the requested tools.
for tool_call in response.tool_calls:
    selected_tool = tools_by_name[tool_call["name"]]

    tool_result = selected_tool.invoke(tool_call["args"])

    print("Executed:", tool_call["name"])
    print("Result:", tool_result)

    # Attach the result to the specific request that produced it.
    messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"],
        )
    )

# 5. Give Ollama the results.
if response.tool_calls:
    next_response = llm_with_tools.invoke(messages)
    print("Answer:", next_response.content)
    print("Additional tool requests:", next_response.tool_calls)
else:
    print("Answer:", response.content)


