def create_report(success: bool, error: str | None, output: any = None) -> dict:

    return {
        "success": success,
        "error": error,
        "output": output
    }