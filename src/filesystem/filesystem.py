from pathlib import Path
from logger import logger


class FileSystem:
    def __init__(self, vault_path):

        self.root = Path(vault_path)

    def list_files(self, path: str = ".") -> dict:
        """List files in the directory
        
        Args: 
            - path: directory path
            
        Returns:
            out (list): list of dicts containing keys:
                - name: file name
                - type: file or directory
                - size_bytes: size of the file in bytes
        """

        full_path = self._create_full_path(path=path)

        if not full_path.is_dir():
            raise NotADirectoryError

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

        return out

    def read_file(self, path: str=".", offset: int=0, read_max_characters: int=5000) -> dict:
        """
        Read the contents of a file within the agent's vault.

        Args:
            path (str): Path to the file relative to the vault root.
            offset (int): the character number of which to start reading the file.
            read_max_characters (int): maximum number of characters to read

        Returns:
            dict with the following keys:
                - offset (int): num character offset
                - characters read (int): num characters read
                - truncated (bool): True if more characters exist to be read
                - content (str): content read
        """

        full_path = self._create_full_path(path=path)

        if not full_path.is_file():
            raise IsADirectoryError

        content = full_path.read_text(encoding="utf-8")

        with open(full_path, "r", encoding="utf-8") as f:
            f.seek(offset)
            content = f.read(read_max_characters+1) #read one more character than necessary to see if there is more content past read_max_characters

        truncated = len(content) > read_max_characters

        if truncated:
            return content[:read_max_characters] + f"...\n\n TRUNCATED [file content exceeds read_max_characters={read_max_characters}]"

        return {
            "offset": offset,
            "characters read": len(content)-1,
            "truncated": truncated,
            "content": content
        }

    def create_file(self, path: str=".", content: str=""):
        """Creates a file and writes to it.
        
        does NOT create parent directories if they dont exist

        Args:
            - path (str): path relative to vault
            - content (str): content to be written into the file

        Returns:
            dict containing the following keys:
                - path (str): path where the file was created
                - content_written (str): Returns the first 50 characters of content
                - characters written (int): Returns the total number of characters written.
        """

        path = Path(path)
        parent = self._create_full_path(path.parent) #handles existance and within vault

        if not parent.is_dir():
            raise NotADirectoryError(f"{parent} is a file, not a directory.")

        full_path = parent / path.name

        if full_path.exists():
            raise FileExistsError(f"{path} already exists! create_file cannot overwrite existing files")

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "path": path,
            "content written": content[:50] + "... [Truncated]",
            "characters written": len(content)
        }

    def _create_full_path(self, path) -> bool | Path:
        """ Checks to see if root + path is 1) a valid path and 2) doesn't escape the vault_directory,
        and then creates the full path resolved.
        """
        
        path = Path(path)

        full_path = self.root / path

        if not full_path.exists():
            raise FileNotFoundError(f"{path} not found.")

        requested_path = full_path.resolve() 

        if not requested_path.is_relative_to(self.root):
            raise PermissionError(f"{path} is outside of allowed directory")

        return requested_path