from pathlib import Path

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
                - report (str): gives the file path input and whether the path is valid or not
                - out (list[dict] or None): Files and subdirectories
                    - name (str): Entry name.
                    - type (str): Either "file" or "directory".
                    - size_bytes (int): File size in bytes, if applicable.

        Restrictions:
            - Access is limited to the configured vault directory.
            - Paths outside the vault are not permitted.
            - This tool cannot read, create, modify, or delete files.
        """

        if not self._is_safe_path(path=path):
            return {
                "status": "failed",
                "report": "invalid path: outside of root.",
                "output": None,
            }
        
        path = Path(path)
        full_path = self.root / path
        
        ret = {
            "status": None,
            "report": None,
            "output": None
        }

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
            
            ret["status"] = "success"
            ret["report"] = f"Valid directory: {path}"
            ret["output"] = out
            
        else:
            ret['status'] = "failed"
            ret['report'] = f"{path} is not a valid directory (does not exist, or path is malformed)"

        return ret

    def _is_safe_path(self, path) -> bool:

        path = Path(path)

        full_path = self.root / path

        requested_path = full_path.resolve() 

        if not requested_path.is_relative_to(self.root):
            return False

        return True