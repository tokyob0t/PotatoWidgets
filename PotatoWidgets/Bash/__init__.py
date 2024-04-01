"""
Utility class for shell-related operations using GLib and Gio libraries.

Methods:
    - expandvars: Expand environment variables and user home directory in a given path.
    - run: Run a command in the shell.
    - get_env: Get the value of an environment variable.
    - get_output: Get the output of a command run in the shell.
    - popen: Open a subprocess to run a command.
    - monitor_file: Monitor changes to a file.
"""

from ..Imports import *

__all__ = ["Bash"]


class Bash:
    """
    Utility class for shell-related operations using GLib and Gio libraries.

    Methods:
        - run: Run a command in the shell.
        - get_env: Get the value of an environment variable.
        - get_output: Get the output of a command run in the shell.
        - popen: Open a subprocess to run a command.
        - monitor_file: Monitor changes to a file.
        - expandvars: Expand environment variables and user home directory in a given path.
    """

    @staticmethod
    def run(cmd: Union[list, str]) -> bool:
        """
        Run a command in the shell.

        Args:
            cmd (Union[list, str]): The command to run.

        Returns:
            bool: The exit status of the command.

        """
        if isinstance(cmd, list):
            cmd = [Bash.expandvars(i) for i in cmd]
        elif isinstance(cmd, str):
            cmd = Bash.expandvars(cmd)

        try:
            # Using Glib's spawn_command_line_sync to run the command synchronously
            result, _ = GLib.spawn_command_line_sync(cmd)
            return result == 0
        except GLib.Error as e:
            print(f"Error executing command: {e.message}")
            return False

    @staticmethod
    def run(cmd: Union[List[str], str]) -> bool:
        """
        Run a command in the shell.

        Args:
            cmd (Union[List[str], str]): The command to run.

        Returns:
            bool: The exit status of the command.

        """
        if isinstance(cmd, (list)):
            cmd = [Bash.expandvars(i) for i in cmd]
        elif isinstance(cmd, (str)):
            cmd = Bash.expandvars(cmd)

        _proc: Gio.Subprocess = Gio.Subprocess.new(
            flags=Gio.SubprocessFlags.STDERR_SILENCE
            | Gio.SubprocessFlags.STDOUT_SILENCE,
            argv=cmd,
        )
        return _proc.wait_check()

    @staticmethod
    def dir_exists(path: str) -> bool:
        """
        Check if a directory exists at the specified path.

        Args:
            path (str): The path to the directory.

        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return GLib.file_test(Bash.expandvars(path), GLib.FileTest.IS_DIR)

    @staticmethod
    def file_exists(path: str) -> bool:
        """
        Check if a file exists at the specified path.

        Args:
            path (str): The path to the file.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return GLib.file_test(Bash.expandvars(path), GLib.FileTest.EXISTS)

    @staticmethod
    def mkdir(path: str) -> bool:
        """
        Create a directory at the specified path.

        Args:
            path (str): The path to the directory.

        Returns:
            bool: True if the directory creation is successful, False otherwise.
        """
        return {0: True, -1: False}.get(
            GLib.mkdir_with_parents(Bash.expandvars(path), 0o755), False
        )

    @staticmethod
    def get_output(cmd: str) -> str:
        """
        Run a shell command and return its output.

        Args:
            cmd (str): The command to run.

        Returns:
            str: The output of the command.
        """
        stdout: bytes
        stderr: bytes
        state: int

        cmd = Bash.expandvars(cmd)

        try:
            _, stdout, stderr, state = GLib.spawn_command_line_sync(cmd)
            return stdout.decode() if state == 0 else stderr.decode()
        except:
            return ""

    @staticmethod
    def get_output(cmd: str) -> str:
        """
        Get the output of a command run in the shell.

        Args:
            cmd (str): The command to run.

        Returns:
            str: The output of the command.

        """
        stdout: bytes
        stderr: bytes
        state: int

        cmd = Bash.expandvars(cmd)

        try:
            _, stdout, stderr, state = GLib.spawn_command_line_sync(cmd)
            return stdout.decode() if state == 0 else stderr.decode()
        except:
            return ""

    @staticmethod
    def monitor_file(
        path: str,
        flags: Literal[
            "none",
            "send_moved",
            "watch_moves",
            "watch_mounts",
            "hard_links",
        ] = "none",
    ):
        """
        Monitor changes to a file.

        Args:
            path (str): The path to the file to monitor.
            flags: Flags to specify monitoring behavior.

        Returns:
            Gio.FileMonitor: The file monitor object.

        """

        file: Gio.File
        monitor: Gio.FileMonitor
        monitor_flags: Gio.FileMonitorFlags

        if isinstance(flags, (str)):
            monitor_flags = {
                "none": Gio.FileMonitorFlags.NONE,
                "send_moved": Gio.FileMonitorFlags.SEND_MOVED,
                "watch_moves": Gio.FileMonitorFlags.WATCH_MOVES,
                "watch_mounts": Gio.FileMonitorFlags.WATCH_MOUNTS,
                "hard_links": Gio.FileMonitorFlags.WATCH_HARD_LINKS,
            }.get(flags, Gio.FileMonitorFlags.NONE)

        path = Bash.expandvars(path)
        file = Gio.File.new_for_path(path)
        monitor = file.monitor(flags=monitor_flags)
        return monitor

    @staticmethod
    def popen(
        cmd: Union[List[str], str],
        stdout: Union[Callable, None] = None,
        stderr: Union[Callable, None] = None,
    ) -> Union[Gio.Subprocess, None]:
        """
        Open a subprocess to run a command.

        Args:
            cmd (Union[List[str], str]): The command to run.
            stdout (Union[Callable, None], optional): Callback function for stdout. Defaults to None.
            stderr (Union[Callable, None], optional): Callback function for stderr. Defaults to None.

        Returns:
            Union[Gio.Subprocess, None]: The subprocess object.

        """
        output: str
        success: bool
        parsed_cmd: List[str]
        proc: Gio.Subprocess
        stdout_pipe: Gio.InputStream
        stderr_pipe: Gio.InputStream
        stdout_stream: Gio.DataInputStream
        stderr_stream: Gio.DataInputStream

        def read_stream(out: Gio.DataInputStream, callback: Callable):
            def internal_callback(stdout: Gio.DataInputStream, res: Gio.Task):
                nonlocal output
                try:
                    output = stdout.read_line_finish_utf8(res)[0]

                    callback(output)
                    stdout.read_line_async(
                        io_priority=GLib.PRIORITY_LOW, callback=internal_callback
                    )

                except Exception as e:
                    print(e)

            out.read_line_async(
                io_priority=GLib.PRIORITY_LOW, callback=internal_callback
            )

        if isinstance(cmd, (str)):
            cmd = Bash.expandvars(cmd)
            success, parsed_cmd = GLib.shell_parse_argv(cmd)
            if success and parsed_cmd:
                cmd = parsed_cmd

        elif isinstance(cmd, (list)):
            parsed_cmd = [Bash.expandvars(i) for i in cmd]
            if parsed_cmd:
                cmd = parsed_cmd

        if cmd:

            proc = Gio.Subprocess.new(
                argv=cmd,
                flags=Gio.SubprocessFlags.STDOUT_PIPE | Gio.SubprocessFlags.STDERR_PIPE,
            )

            if stdout is not None:
                stdout_pipe = proc.get_stdout_pipe()
                stdout_stream = Gio.DataInputStream.new(base_stream=stdout_pipe)
                read_stream(stdout_stream, stdout)

            if stderr is not None:
                stderr_pipe = proc.get_stderr_pipe()
                stderr_stream = Gio.DataInputStream.new(base_stream=stderr_pipe)
                read_stream(stderr_stream, stderr)

            if stderr is None and stdout is None:
                _ = proc.communicate()

            return proc

    @staticmethod
    def expandvars(path: str) -> str:
        """
        Expand environment variables and user home directory in a given path.

        Args:
            path (str): The path containing environment variables and user home directory.

        Returns:
            str: The path with expanded variables and user home directory.

        """
        return os_expanduser(os_expandvars(path))

    @staticmethod
    def get_env(var: str) -> str:
        """
        Get the value of an environment variable.

        Args:
            var (str): The name of the environment variable.

        Returns:
            str: The value of the environment variable.

        """
        return GLib.getenv(variable=var)
