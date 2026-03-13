"""Windows terminal wrapper using subprocess and ConPTY.

Uses pywinpty for proper pseudo-terminal support on Windows, falling
back to subprocess pipes when pywinpty is not available.

Requires Windows 10 1809+ for ANSI escape sequence support.
"""

import os
import subprocess
import sys
import threading

from termisan.platform import enable_windows_ansi, enable_windows_input_mode, get_terminal_size
from termisan.themes import AnimeTheme
from termisan.wrapper import (
    ThemedTerminalWrapper,
    _ansi_move,
    _ansi_reset,
    _ansi_reset_scroll_region,
    _ansi_set_scroll_region,
    _ansi_show_cursor,
)


class WindowsTerminalWrapper(ThemedTerminalWrapper):
    """Subprocess-based terminal wrapper for Windows.

    Uses ConPTY via pywinpty when available for full PTY support,
    or falls back to subprocess with threaded I/O forwarding.
    """

    def __init__(self, theme: AnimeTheme, command: list[str]):
        super().__init__(theme, command)
        self._process = None
        self._stop_event = threading.Event()
        self._conpty = None

    def run(self) -> int:
        """Run the themed terminal wrapper. Returns the child exit code."""
        # Enable ANSI escape sequences on Windows
        if not enable_windows_ansi():
            print(
                "Warning: Could not enable ANSI support. "
                "Use Windows Terminal or ConEmu for best results.",
                file=sys.stderr,
            )

        enable_windows_input_mode()

        self._update_terminal_size()

        # Try ConPTY via pywinpty first, fall back to subprocess pipes
        try:
            return self._run_with_conpty()
        except ImportError:
            return self._run_with_subprocess()

    def _run_with_conpty(self) -> int:
        """Run using pywinpty for full ConPTY support."""
        import winpty

        content_rows = self.content_bottom - self.content_top + 1

        self._conpty = winpty.PtyProcess.spawn(
            self.command,
            dimensions=(content_rows, self.cols),
        )

        self._running = True
        self._draw_frame()

        # Start reader thread
        reader = threading.Thread(target=self._conpty_reader, daemon=True)
        reader.start()

        try:
            self._conpty_input_loop()
        finally:
            self._running = False
            self._stop_event.set()
            if self._conpty.isalive():
                self._conpty.terminate()
            self._cleanup_terminal()

        return self._conpty.exitstatus or 0

    def _conpty_reader(self):
        """Read output from ConPTY and write to stdout."""
        while self._running and not self._stop_event.is_set():
            try:
                data = self._conpty.read(4096)
                if data:
                    sys.stdout.write(data)
                    sys.stdout.flush()
            except EOFError:
                break
            except Exception:
                if not self._running:
                    break

    def _conpty_input_loop(self):
        """Read keyboard input and forward to ConPTY."""
        import msvcrt

        while self._running and self._conpty.isalive():
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch == "\x00" or ch == "\xe0":
                    # Extended key — read the scan code
                    scan = msvcrt.getwch()
                    ansi = _extended_key_to_ansi(ch, scan)
                    if ansi:
                        self._conpty.write(ansi)
                else:
                    self._conpty.write(ch)
            else:
                # Brief sleep to avoid busy-waiting
                self._stop_event.wait(0.01)

    def _run_with_subprocess(self) -> int:
        """Fallback: run using subprocess with piped I/O and threading."""
        content_rows = self.content_bottom - self.content_top + 1

        # Set terminal size via environment for the child
        env = os.environ.copy()
        env["LINES"] = str(content_rows)
        env["COLUMNS"] = str(self.cols)
        # Hint to child programs that we support color
        env["TERM"] = "xterm-256color"

        self._process = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            bufsize=0,
        )

        self._running = True
        self._draw_frame()

        # Position cursor in content area
        sys.stdout.write(_ansi_move(self.content_top, 1))
        sys.stdout.flush()

        # Start output reader thread
        reader = threading.Thread(target=self._pipe_reader, daemon=True)
        reader.start()

        try:
            self._pipe_input_loop()
        finally:
            self._running = False
            self._stop_event.set()
            if self._process.poll() is None:
                self._process.terminate()
                try:
                    self._process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self._process.kill()
            self._cleanup_terminal()

        return self._process.returncode or 0

    def _pipe_reader(self):
        """Read child stdout and write to our stdout."""
        while self._running:
            try:
                data = self._process.stdout.read(4096)
                if not data:
                    break
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
            except (OSError, ValueError):
                break

    def _pipe_input_loop(self):
        """Read keyboard input and forward to child stdin."""
        import msvcrt

        while self._running and self._process.poll() is None:
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch == "\x00" or ch == "\xe0":
                    scan = msvcrt.getwch()
                    ansi = _extended_key_to_ansi(ch, scan)
                    if ansi:
                        try:
                            self._process.stdin.write(ansi.encode())
                            self._process.stdin.flush()
                        except (OSError, BrokenPipeError):
                            break
                else:
                    try:
                        self._process.stdin.write(ch.encode())
                        self._process.stdin.flush()
                    except (OSError, BrokenPipeError):
                        break
            else:
                self._stop_event.wait(0.01)

    def _cleanup_terminal(self):
        """Reset terminal state on Windows."""
        sys.stdout.write(_ansi_reset_scroll_region())
        sys.stdout.write(_ansi_show_cursor())
        sys.stdout.write(_ansi_reset())
        sys.stdout.write(_ansi_move(self.rows, 1))
        sys.stdout.write("\n")
        sys.stdout.flush()


def _extended_key_to_ansi(prefix: str, scan: str) -> str | None:
    """Convert Windows extended key codes to ANSI escape sequences."""
    code = ord(scan)
    mapping = {
        72: "\033[A",   # Up arrow
        80: "\033[B",   # Down arrow
        77: "\033[C",   # Right arrow
        75: "\033[D",   # Left arrow
        71: "\033[H",   # Home
        79: "\033[F",   # End
        82: "\033[2~",  # Insert
        83: "\033[3~",  # Delete
        73: "\033[5~",  # Page Up
        81: "\033[6~",  # Page Down
        59: "\033OP",   # F1
        60: "\033OQ",   # F2
        61: "\033OR",   # F3
        62: "\033OS",   # F4
        63: "\033[15~", # F5
        64: "\033[17~", # F6
        65: "\033[18~", # F7
        66: "\033[19~", # F8
        67: "\033[20~", # F9
        68: "\033[21~", # F10
        133: "\033[23~", # F11
        134: "\033[24~", # F12
    }
    return mapping.get(code)
