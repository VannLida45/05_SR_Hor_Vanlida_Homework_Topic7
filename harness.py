
from pydantic import ValidationError



from config import PERMISSIONS, TOOL_REGISTRY

def execute_tool(role, tool_name, arguments):

    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": "UNKNOWN_TOOL",
            "message": "This tool is not available.",
        }
    if tool_name not in PERMISSIONS.get(role, set()):
        return {
            "success": False,
            "error": "PERMISSION_DENIED",
            "message": f"{role} cannot use {tool_name}.",
        }

    schema, function = TOOL_REGISTRY[tool_name]

    try:
        validated = schema.model_validate(arguments)

    except ValidationError:
        return {
            "success": False,
            "error": "INVALID_ARGUMENTS",
            "message": "The provided arguments are invalid.",
        }

    try:
        return function(**validated.model_dump())

    except Exception as exc:
        print(f"Tool execution error: {type(exc).__name__}")

        return {
            "success": False,
            "error": "DATABASE_ERROR",
            "message": "The database operation failed.",
        }