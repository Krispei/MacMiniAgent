import subprocess
from pathlib import Path
import uuid


class RunCommand():
    def __init__(self, workspace_path: str, max_output_chars: int):

        #Workspace must exist
        self.WORKSPACE = Path.home() / workspace_path
        print(self.WORKSPACE)
        self.MAX_OUTPUT_CHARS = max_output_chars

    def run_command(self, argv: list[str], timeout: int=5) -> dict:
        """Executes python command in docker container"""

        container_name = f"agent-{uuid.uuid4().hex}"

        if not argv or argv[0] not in {"python", "python3", "pytest"}:
            return {
                "exit_code": None,
                "stdout": "",
                "stderr": "Command is not permitted",
                "timed_out": False
            }

        command = [
            "docker", "run", 
            "--rm",
            "--name", container_name,
            "--pull", "never",
            "--network", "none",
            "--cpus", "1",
            "--memory", "512m",
            "--pids-limit", "64",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--read-only",
            "--tmpfs", "/tmp:rw,nosuid,nodev,size=64m",
            "--mount", 
            f"type=bind,src={self.WORKSPACE.resolve()},dst=/workspace",
            "--workdir", "/workspace",
            "python:3.13-slim",
            *argv,
        ]

        try:
            result = subprocess.run(
                command, 
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "exit_code": result.returncode,
                "stdout": result.stdout[-self.MAX_OUTPUT_CHARS:],
                "stderr": result.stderr[-self.MAX_OUTPUT_CHARS:],
                "timed_out": False,
            }
        except subprocess.TimeoutExpired:
            subprocess.run(
                ["docker", "rm", "-f", container_name],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                "exit_code": None,
                "stdout": "",
                "stderr": "Command exceeded timeout\n",
                "timed_out": True,
            }
        except (OSError, ValueError) as exc:
            return {
                "exit_code": None,
                "stdout": "",
                "stderr": str(exc),
                "timed_out": False
            }
