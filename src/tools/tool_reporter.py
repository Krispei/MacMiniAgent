def create_report(status: str = "", details: str = "", output: any = None) -> dict:

    return {
        "status": status,
        "details": details,
        "output": output
    }