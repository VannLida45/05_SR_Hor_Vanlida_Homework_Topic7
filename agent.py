import json

from ollama import chat

from config import MODEL_NAME, MAX_ITERATIONS
from harness import execute_tool


from config import TOOL_SCHEMAS, SYSTEM_MESSAGE

def run_agent(user_request, role, messages):

    messages.append({
        "role": "user",
        "content": user_request,
    })

    for iteration in range(1, MAX_ITERATIONS + 1):

        print(f"\n--- Iteration {iteration} ---")

        try:
            response = chat(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOL_SCHEMAS,
            )

        except Exception as exc:
            print(f"LLM error: {type(exc).__name__}")
            return "The language model is unavailable."

        message = response.message

        messages.append(
            message.model_dump(exclude_none=True)
        )

        if not message.tool_calls:

            answer = message.content or "No answer generated."

            print("\nFINAL ANSWER:")
            print(answer)

            return answer

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            print("\nTOOL REQUEST")
            print("Tool:", tool_name)
            print("Arguments:", arguments)

            result = execute_tool(
                role=role,
                tool_name=tool_name,
                arguments=arguments,
            )

            print("\nTOOL RESULT")
            print(result)

            messages.append({
                "role": "tool",
                "tool_name": tool_name,
                "content": json.dumps(result),
            })

    print("\nMAXIMUM ITERATIONS REACHED")

    return (
        "The agent stopped because it reached "
        "the maximum number of iterations."
    )