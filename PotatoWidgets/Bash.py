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

from .Imports import *


class Bash:
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

    @staticmethod
    def run(cmd: Union[List[str], str]) -> int:
        """
        Run a command in the shell.

        Args:
            cmd (Union[List[str], str]): The command to run.

        Returns:
            int: The exit status of the command.

        """
        state: int
        if isinstance(cmd, (list)):
            cmd = [Bash.expandvars(i) for i in cmd]
        elif isinstance(cmd, (str)):
            cmd = Bash.expandvars(cmd)

        try:
            _, _, _, state = GLib.spawn_command_line_sync(cmd)
            return state
        except:
            return -1

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
        flags: Union[
            Literal["none", "send_moved", "watch_moves", "watch_mounts", "hard_links"],
            Gio.FileMonitorFlags,
        ] = Gio.FileMonitorFlags.NONE,
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

        if isinstance(flags, (str)):
            flags = {
                "none": Gio.FileMonitorFlags.NONE,
                "send_moved": Gio.FileMonitorFlags.SEND_MOVED,
                "watch_moves": Gio.FileMonitorFlags.WATCH_MOVES,
                "watch_mounts": Gio.FileMonitorFlags.WATCH_MOUNTS,
                "hard_links": Gio.FileMonitorFlags.WATCH_HARD_LINKS,
            }.get(flags, Gio.FileMonitorFlags.NONE)

        path = Bash.expandvars(path)
        file = Gio.File.new_for_path(path)
        monitor = file.monitor(flags=flags)
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
                    return (
                        callback(output),
                        stdout.read_line_async(
                            io_priority=GLib.PRIORITY_LOW, callback=internal_callback
                        ),
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

            return proc
