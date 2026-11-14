from pathlib import Path
from logger import logger
from tools.tool_reporter import create_report

class FilesystemTools:
    def __init__(self, FileSystem):

        self.FileSystem = FileSystem

    def list_files(self, path: str = "") -> dict:
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
                - tool_call (str): the name of the tool called.
                - success (bool): True for successful tool call, False for unsuccessful tool call.
                - error (str | None): Error message if the tool call fails, otherwise None on successfull tool call
                - output (list | None): list of dicts containing:
                    - name: file name
                    - type: file or directory
                    - size_bytes: size of the file in bytes

        Restrictions:
            - Access is limited to the configured vault directory.
            - Paths outside the vault are not permitted.
            - This tool cannot read, create, modify, or delete files.
        """

        try:
            out = self.FileSystem.list_files(path=path)
            report = create_report(
                tool_call="list_files",
                success=True,
                error=None,
                output=out
            )
            logger.info("list_files called: %s",report)
            return report
        
        except (FileNotFoundError, PermissionError, NotADirectoryError) as e:
            report = create_report(
                tool_call="list_files",
                success=False,
                error=str(e),
                output=None
            )
            logger.info("list called: %s", report)
            return report

    def read_file(self, path: str="") -> dict:

        """
        Read the contents of a file within the agent's vault.

        Use this tool when you need to inspect the contents of a known file,
        retrieve information from a document, or examine a file discovered
        through list_files or search_files.

        Args:
            path (str): Path to the file relative to the vault root.

        Returns:
            dict: A dictionary containing:
                - tool_call (str): the name of the tool called.
                - success (bool): True for successful tool call, False for unsuccessful tool call.
                - error (str | None): Error message if the tool call fails, otherwise None on successfull tool call
                - output (dict | None): dict with the following keys:
                    - offset (int): num character offset
                    - characters read (int): num characters read
                    - truncated (bool): True if more characters exist to be read
                    - content (str): content read

        Restrictions:
            - Only files within the configured vault may be accessed.
            - Only UTF-8 text files are supported.
            - This tool cannot modify files.
        """

        try:
            out = self.FileSystem.read_file(path=path)
            report = create_report(
                tool_call="read_file",
                success=True,
                error=None,
                output=out
            )
            logger.info("read_files called: %s",report)
            return report
        
        except (FileNotFoundError, PermissionError, IsADirectoryError) as e:
            report = create_report(
                tool_call="read_file",
                success=True,
                error=str(e),
                output=None
            )
            logger.info("read_files called: %s",report)
            return report

    def create_file(self, path: str="", content: str="") -> dict:
        """
        Create a new file at the specified path.

        Use this tool when a new file needs to be created. The file must not
        already exist. To modify an existing file, use edit_file instead.

        Args:
            path: Path to the new file, relative to the vault root.
            content: Complete text content to write into the new file.

        Returns:
            dict: A dictionary containing:
                - tool_call (str): the name of the tool called.
                - success (bool): True for successful tool call, False for unsuccessful tool call.
                - error (str | None): Error message if the tool call fails, otherwise None on successfull tool call
                - output (dict | None): dict with the following keys:
                    - path (str): path where the file was created
                    - content_written (str): Returns the first 50 characters of content
                    - characters written (int): Returns the total number of characters written.
        Notes:
            - Never overwrites existing files.
            - Does not create parent directories if they dont exist.
            - Rejects paths outside the workspace.
            - Does not follow symlinks outside the workspace.
            - Writes text using UTF-8 encoding.
        """

        try:
            out = self.FileSystem.create_file(path=path, content=content)
            report = create_report(
                tool_call="create_file",
                success=True,
                error=None,
                output=out
            )
            logger.info("Tool call create_file: %s", report)
            return report
        except (FileNotFoundError, FileExistsError, NotADirectoryError, PermissionError) as e:
            report = create_report(
                tool_call="create_file",
                success=False,
                error=str(e),
                output=None
            )
            logger.info("Tool call create_file FAILED: %s", report)
            return report