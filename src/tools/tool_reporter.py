def create_report(tool_call, success: bool, error: str | None, output: any = None) -> dict:

    return {
        "Tool call": tool_call,
        "success": success,
        "error": error,
        "output": output
    }