from server.tool_descriptor import get_tool_description

TOOL_DESCRIPTION = get_tool_description()


BASIC_REQUEST_TEMPLATE = """
{
    id : <id>,
    requests:[
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        {
            id:<request_id>,
            method : "tools/<tool_name>",
            params : {
                param1:value1,
                param2:value2,
                ...
            }
        },
        ...
    ]
}
"""

BASIC_RESPONSE_TEMPLATE="""
{
    id:<id>
    results:[
        {
            id:<request_id>,
            method: "tools/<tool_name>",
            results:[...]
        },
        {
            id:<request_id>,
            method: "tools/<tool_name>",
            results:[...]
        },
        ...
    ]
}
"""

BASIC_PROMPT=f"""You are an intelligent agent system equipped with the following tools. Based on a user's query, you must generate a structured list of tool calls in JSON format. Each call must include the tool method, required parameters, and a unique request ID. All requests will be sent together in a single JSON payload.

Here are the available tools:
{TOOL_DESCRIPTION}

Your task is: **Given a user's natural language query, generate a structured tool invocation JSON** in the following format:

```json
{BASIC_REQUEST_TEMPLATE}
```
**User Query** :
"""
