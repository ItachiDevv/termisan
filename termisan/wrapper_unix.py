"""Unix (macOS / Linux) PTY-based terminal wrapper.

Uses pty.fork(), termios, and select for a true PTY-based wrapper
that preserves full terminal interactivity.
"""

import errno
import fcntl
import os
import pty
import select
import signal
import struct
import sys
import termios
import tty

from termisan.themes import AnimeTheme
from termisan.wrapper import ThemedTerminalWrapper


class UnixTerminalWrapper(ThemedTerminalWrapper):
    """PTY-based terminal wrapper for macOS and Linux."""

    def __init__(self, theme: AnimeTheme, command: list[str]):
        super().__init__(theme, command)
        self.child_pid = -1
        self.master_fd = -1
        self._original_termios = None

    def run(self) -> int:
        """Run the themed terminal wrapper. Returns the child exit code."""
        # Get terminal size
        self._update_terminal_size()

        # Save terminal state
        old_settings = termios.tcgetattr(sys.stdin.fileno())
        self._original_termios = old_settings

        try:
            # Fork PTY
            self.child_pid, self.master_fd = pty.fork()

            if self.child_pid == 0:
                # Child process: exec the command
                os.execvp(self.command[0], self.command)
                sys.exit(127)

            # Parent process
            self._running = True

            # Set up signal handlers
            signal.signal(signal.SIGWINCH, self._handle_resize)
            signal.signal(signal.SIGCHLD, signal.SIG_DFL)

            # Set the child PTY size
            self._set_child_size()

            # Put terminal in raw mode
            tty.setraw(sys.stdin.fileno())

            # Draw initial frame
            self._draw_frame()

            # Main I/O loop
            return self._io_loop()

        finally:
            # Restore terminal
            self._running = False
            self._cleanup_terminal()
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, old_settings)
            except termios.error:
                pass

    def _io_loop(self) -> int:
        """Main I/O forwarding loop between stdin and the child PTY."""
        stdin_fd = sys.stdin.fileno()
        stdout_fd = sys.stdout.fileno()

        while self._running:
            try:
                rfds, _, _ = select.select([stdin_fd, self.master_fd], [], [], 0.1)
            except (select.error, OSError) as e:
                if hasattr(e, "errno") and e.errno == errno.EINTR:
                    continue
                if isinstance(e, OSError) and e.errno == errno.EINTR:
                    continue
                break

            if stdin_fd in rfds:
                try:
                    data = os.read(stdin_fd, 4096)
                    if not data:
                        break
                    os.write(self.master_fd, data)
                except OSError:
                    break

            if self.master_fd in rfds:
                try:
                    data = os.read(self.master_fd, 4096)
                    if not data:
                        break
                    # Write to stdout (the scroll region will contain it)
                    os.write(stdout_fd, data)
                except OSError:
                    break

        # Wait for child and get exit code
        try:
            _, status = os.waitpid(self.child_pid, 0)
            if os.WIFEXITED(status):
                return os.WEXITSTATUS(status)
            return 1
        except ChildProcessError:
            return 0

    def _update_terminal_size(self):
        """Update stored terminal dimensions using ioctl."""
        try:
            result = struct.unpack(
                "hh", fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, b"\x00" * 4)
            )
            self.rows = result[0]
            self.cols = result[1]
        except (OSError, struct.error):
            self.rows = 24
            self.cols = 80

    def _set_child_size(self):
        """Set the child PTY size to match the content area."""
        content_rows = self.content_bottom - self.content_top + 1
        try:
            winsize = struct.pack("HHHH", content_rows, self.cols, 0, 0)
            fcntl.ioctl(self.master_fd, termios.TIOCSWINSZ, winsize)
        except OSError:
            pass

    def _handle_resize(self, signum, frame):
        """Handle terminal resize (SIGWINCH)."""
        self._update_terminal_size()
        self._set_child_size()

        # Signal the child about the resize
        try:
            os.kill(self.child_pid, signal.SIGWINCH)
        except OSError:
            pass

        # Redraw frame
        self._draw_frame()
