import subprocess
from pathlib import Path
import time

class RunCommand():
    def __init__(self, workspace_path: str, max_output_chars: int = 1000):

        #Workspace must exist
        self.WORKSPACE = Path.home() / workspace_path
        print(self.WORKSPACE)
        self.MAX_OUTPUT_CHARS = max_output_chars

    def run_command(self, argv: list[str], timeout: int=5) -> dict:
        """Executes python command in docker container
        
        Args:
            argv (list[str]), default: list of arguments of the command to run
            timeout (int), default = 5: defines the maximum time to wait for the command to run.

        Returns:
            dict with the following keys which answer the following questions:
                "success": Did the harness run the command and get a result? (Doesn't mean the program successfully ran, etc)
                "exit_code": what status came back, if any?
                "stdout": standard out 
                "stderr": standard err
                "timed_out": Did a time limit expire?     
        
        Exit codes (GNU timeout, without --preserve-status)

        124   The command timed out.
        125   The timeout program itself failed.
        126   The command was found but could not be invoked.
        127   The command could not be found.
        137   The command, or timeout itself, was sent SIGKILL (128 + 9).
        other The command's own exit status.

        Exit codes (sbx exec, from `sbx exec --help`)

        125   sbx could not run the command (for example, the sandbox does not exist).
        127   The command is missing (cloud backends may report 125 instead).
        other The command's exit status.
        
        Notes:
            - elapsed time includes sbx startup and reporting, so an early kill could look like it happened after the limit.
            - A script can deliberately return 124 or 137. this could lead to incorrect labelling.
        
        """

        if timeout <= 0:
            return {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": f"{timeout} cannot be zero or negative.",
                "timed_out": False
            }


        valid_commands = {"python", "python3", "pytest"}
        
        if not argv or argv[0] not in valid_commands:
            return {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": f"Invalid command. Command must start with {valid_commands}",
                "timed_out": False
            }

        grace_period = 15
        startup_duration = 10
        reporting = 5
        outer_limit = startup_duration + timeout + grace_period + reporting

        command = [
            "sbx", "exec", "shell-agent-scratch",
            "timeout", "--kill-after", str(grace_period), str(timeout),
            *argv
        ]

        try:
            start = time.perf_counter()
            result = subprocess.run(
                command, 
                capture_output=True,
                text=True,
                timeout=outer_limit
            )
            elapsed = time.perf_counter() - start

            exit_code = result.returncode
            success = exit_code not in [125, 126, 127]
            timed_out = exit_code == 124 or (exit_code == 137 and elapsed >= timeout)

            stdout = result.stdout[-self.MAX_OUTPUT_CHARS:]
            stderr = result.stderr[-self.MAX_OUTPUT_CHARS:]
            
            if exit_code == 137: 
               stderr += "Process was reported killed by SIGKILL. Possible causes include: forced termination after time limit or running out of memory. It may have made partial changes; check them before retrying."
            
            return {
                "success": success,
                "exit_code": exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "timed_out": timed_out,
            }
        
        except subprocess.TimeoutExpired:
            # outer timeout fired. Unkonwn state of the command. Tell model to proceed with caution.
            return {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": "Harness timeout fired. State of the command is unknown. Files may or may not have changed due to the command. Check the state of files that the command is known to modify.",
                "timed_out": True,
            }
            
        except (OSError, ValueError) as exc:
            # catches sbx not installed

            return {
                "success": False,
                "exit_code": None,
                "stdout": "",
                "stderr": str(exc),
                "timed_out": False
            }
