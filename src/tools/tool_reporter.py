from logger import logger

def create_report(tool_call: str, success: bool, error: str | None, output: any = None) -> dict:

    report = {
        "success": success,
        "error": error,
        "output": output
    }

    if success:
        logger.info("Tool call %s SUCCESS: %s", tool_call, report)
    else:
        logger.info("Tool call %s FAILED: %s", tool_call, report)

    return report
