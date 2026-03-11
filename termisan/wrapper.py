"""PTY-based terminal wrapper that adds anime-themed decorations.

Uses ANSI escape sequences and VT100 scroll regions to render a themed
header and footer around the wrapped subprocess (claude, codex, etc.).
"""

import errno
import fcntl
import os
import pty
import random
import select
import signal
import struct
import sys
import termios
import tty
from datetime import datetime

from termisan.sprites import get_sprite_lines
from termisan.themes import AnimeTheme

# ANSI escape helpers
ESC = "\033"
CSI = f"{ESC}["


def _ansi_move(row: int, col: int) -> str:
    return f"{CSI}{row};{col}H"


def _ansi_clear_line() -> str:
    return f"{CSI}2K"


def _ansi_set_scroll_region(top: int, bottom: int) -> str:
    return f"{CSI}{top};{bottom}r"


def _ansi_reset_scroll_region() -> str:
    return f"{CSI}r"


def _ansi_save_cursor() -> str:
    return f"{ESC}7"


def _ansi_restore_cursor() -> str:
    return f"{ESC}8"


def _ansi_hide_cursor() -> str:
    return f"{CSI}?25l"


def _ansi_show_cursor() -> str:
    return f"{CSI}?25h"


def _ansi_color_fg(hex_color: str) -> str:
    """Convert hex color to ANSI 24-bit foreground color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{CSI}38;2;{r};{g};{b}m"


def _ansi_color_bg(hex_color: str) -> str:
    """Convert hex color to ANSI 24-bit background color."""
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{CSI}48;2;{r};{g};{b}m"


def _ansi_reset() -> str:
    return f"{CSI}0m"


def _ansi_bold() -> str:
    return f"{CSI}1m"


def _ansi_dim() -> str:
    return f"{CSI}2m"


class ThemedTerminalWrapper:
    """Wraps a subprocess in a themed terminal frame."""

    HEADER_HEIGHT = 3  # Title bar lines
    FOOTER_HEIGHT = 1  # Status bar line

    def __init__(self, theme: AnimeTheme, command: list[str]):
        self.theme = theme
        self.command = command
        self.rows = 24
        self.cols = 80
        self.child_pid = -1
        self.master_fd = -1
        self._original_termios = None
        self._running = False
        self._quote = random.choice(theme.quotes) if theme.quotes else ""

    @property
    def content_top(self) -> int:
        return self.HEADER_HEIGHT + 1

    @property
    def content_bottom(self) -> int:
        return self.rows - self.FOOTER_HEIGHT

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
            sys.stdout.write(_ansi_reset_scroll_region())
            sys.stdout.write(_ansi_show_cursor())
            sys.stdout.write(_ansi_reset())
            sys.stdout.write(_ansi_move(self.rows, 1))
            sys.stdout.write("\n")
            sys.stdout.flush()
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
        """Update stored terminal dimensions."""
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

    def _draw_frame(self):
        """Draw the themed header and footer, set scroll region."""
        out = []

        # Save cursor
        out.append(_ansi_save_cursor())
        out.append(_ansi_hide_cursor())

        # Draw header
        out.append(self._render_header())

        # Draw footer
        out.append(self._render_footer())

        # Set scroll region to content area
        out.append(_ansi_set_scroll_region(self.content_top, self.content_bottom))

        # Move cursor to content area
        out.append(_ansi_move(self.content_top, 1))

        # Show cursor
        out.append(_ansi_show_cursor())

        sys.stdout.write("".join(out))
        sys.stdout.flush()

    def _render_header(self) -> str:
        """Render the themed header bar."""
        t = self.theme
        out = []

        # Line 1: Top border with anime name
        out.append(_ansi_move(1, 1))
        out.append(_ansi_clear_line())
        out.append(_ansi_color_fg(t.color_primary))
        out.append(_ansi_bold())

        title = f" {t.prompt_icon} {t.name} {t.prompt_icon} "
        border_char = "━"
        side_len = max(0, (self.cols - len(title)) // 2)
        line1 = border_char * side_len + title + border_char * (self.cols - side_len - len(title))
        out.append(line1[:self.cols])
        out.append(_ansi_reset())

        # Line 2: Welcome message / quote
        out.append(_ansi_move(2, 1))
        out.append(_ansi_clear_line())
        out.append(_ansi_color_fg(t.color_secondary))
        msg = f" {t.welcome}"
        out.append(msg[:self.cols])
        out.append(_ansi_reset())

        # Line 3: Bottom border of header
        out.append(_ansi_move(3, 1))
        out.append(_ansi_clear_line())
        out.append(_ansi_color_fg(t.color_primary))
        out.append(_ansi_dim())
        quote_display = f' "{self._quote}" '
        side_len2 = max(0, (self.cols - len(quote_display)) // 2)
        line3 = "─" * side_len2 + quote_display + "─" * (self.cols - side_len2 - len(quote_display))
        out.append(line3[:self.cols])
        out.append(_ansi_reset())

        return "".join(out)

    def _render_footer(self) -> str:
        """Render the themed status bar footer."""
        t = self.theme
        out = []

        footer_row = self.rows
        out.append(_ansi_move(footer_row, 1))
        out.append(_ansi_clear_line())

        # Background color for status bar
        out.append(_ansi_color_bg(t.color_primary))
        out.append(_ansi_color_fg("#FFFFFF"))
        out.append(_ansi_bold())

        left = f" {t.status_left}"
        right = f"{t.status_right} "
        now = datetime.now().strftime("%H:%M")
        center = f" TERMISAN | {now} "

        # Calculate spacing
        total = len(left) + len(center) + len(right)
        if total < self.cols:
            gap_left = (self.cols - total) // 2
            gap_right = self.cols - total - gap_left
            bar = left + " " * gap_left + center + " " * gap_right + right
        else:
            bar = (left + " " + center + " " + right)[:self.cols]

        out.append(bar.ljust(self.cols)[:self.cols])
        out.append(_ansi_reset())

        return "".join(out)


def run_wrapped_session(theme: AnimeTheme, command: list[str]) -> int:
    """Run a command wrapped in an anime-themed terminal frame.

    Args:
        theme: The anime theme to apply.
        command: The command to execute (e.g., ["claude"], ["codex"]).

    Returns:
        The exit code of the wrapped process.
    """
    wrapper = ThemedTerminalWrapper(theme, command)
    return wrapper.run()
