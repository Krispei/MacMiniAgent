"""
    Execute a Python code snippet in an isolated Docker container.

    The code runs inside a fresh, sandboxed container that has:
      - No network access (no outbound or inbound connections).
      - No access to the host filesystem outside the mount.

    USE THIS TOOL WHEN:
      - You need to perform a computation, data transformation, or
        string operation that is easier in Python than by hand.
      - You want to validate or test a small piece of logic.
      - You need to parse, format, or manipulate structured data
        (CSV, JSON, dates, regex, etc.).
      - You want to execute a .py file that exists inside of the mount.

    CONSTRAINTS:
      - Only Python commands are accepted. Shell commands, shell
        escapes (e.g. os.system, subprocess), and any attempt to
        reach outside the container will fail.
      - No internet: pip install, HTTP requests, and any network
        I/O will raise an error.
      - No shared state: each call starts a clean container. Import
        any modules and define all variables inside the code if you are not executing a file    .
      - Only the standard library and pre-installed packages are
        available. Check what's installed rather than assuming.

    Parameters
    ----------
    code : str
        The Python source code to execute. May be a single
        expression, a block of statements, or a full script.
        The output of the last expression is returned as the
        result string.
    timeout_seconds : float, optional
        Maximum wall-clock time the container is allowed to run
        before being killed. Default is 30.0 seconds.

    Returns
    -------
    str
        The captured stdout/stderr from the execution, or an
        error message if the code failed or timed out.
    """