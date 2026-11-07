from pathlib import Path
from logger import logger
from tool_reporter import create_report

class FilesystemTools:
    def __init__(self, vault_path):

        self.root = Path(vault_path)

    def list_files(self, path: str = ".") -> dict:
        """
        List files and subdirectories within the agent's vault.

        Use this tool to explore the vault's directory structure, discover
        available files, and locate documents before reading them. This tool
        returns file metadata only and does not read file contents.

        Args:
            path (str): Directory path relative to the vault root.
                Defaults to "." (the vault root).

        Returns:
            dict: A dictionary containing:
                - status (str): "success" or "failed" indicating success
                - details (str): gives further details on the succes or failure.
                - output (list[dict] or None): Files and subdirectories
                    - name (str): Entry name.
                    - type (str): Either "file" or "directory".
                    - size_bytes (int): File size in bytes, if applicable.

        Restrictions:
            - Access is limited to the configured vault directory.
            - Paths outside the vault are not permitted.
            - This tool cannot read, create, modify, or delete files.
        """

        full_path = self._is_valid_and_safe_path(path=path)

        if not full_path:
            report = create_report(
                status="failed",
                details=f"File path invalid: {path}",
                output=None
            )
            logger.debug("list_files tool call failed: %s",
                    report
            )
            return report

        if full_path.is_dir():
            out = []

            for item in full_path.iterdir():

                name = item.name
                filetype = "file" if item.is_file() else "directory"
                size_bytes = item.stat().st_size
                
                out.append({
                    "name": name,
                    "type": filetype,
                    "size_bytes": size_bytes
                })
            
            report = create_report(
                status="success",
                details=f"Valid path: {path}",
                output=out
            )

        else:
            report = create_report(
                status="failed",
                details=f"Path is not a directory: {path}",
                output=None
            )

        logger.debug("list_files tool call: %s",
                report
        )

        return report

    def _is_valid_and_safe_path(self, path) -> bool | Path:
        """ Checks to see if root + path is 1) a valid path and 2) doesn't escape the vault_directory
        """
        
        path = Path(path)

        full_path = self.root / path

        if not full_path.exists():
            return False

        requested_path = full_path.resolve() 

        if not requested_path.is_relative_to(self.root):
            return False

        return requested_path