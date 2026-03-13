"""Platform detection and compatibility utilities for Termisan.

Provides helpers for cross-platform terminal support across
macOS, Linux, and Windows.
"""

import os
import sys

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

# Unix-like platforms that support PTY, termios, etc.
IS_UNIX = IS_MACOS or IS_LINUX or sys.platform.startswith(("freebsd", "openbsd"))


def get_terminal_size() -> tuple[int, int]:
    """Return (rows, cols) for the current terminal."""
    try:
        size = os.get_terminal_size()
        return size.lines, size.columns
    except OSError:
        return 24, 80


def enable_windows_ansi() -> bool:
    """Enable ANSI escape sequence processing on Windows 10+.

    Returns True if ANSI support was successfully enabled.
    No-op on non-Windows platforms.
    """
    if not IS_WINDOWS:
        return True

    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        ENABLE_PROCESSED_OUTPUT = 0x0001

        for handle_id in (STD_OUTPUT_HANDLE, STD_ERROR_HANDLE):
            handle = kernel32.GetStdHandle(handle_id)
            mode = wintypes.DWORD()
            if not kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                continue
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING | ENABLE_PROCESSED_OUTPUT
            kernel32.SetConsoleMode(handle, new_mode)

        return True
    except Exception:
        return False


def enable_windows_input_mode() -> bool:
    """Enable virtual terminal input processing on Windows.

    Returns True on success. No-op on non-Windows.
    """
    if not IS_WINDOWS:
        return True

    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]

        STD_INPUT_HANDLE = -10
        ENABLE_VIRTUAL_TERMINAL_INPUT = 0x0200

        handle = kernel32.GetStdHandle(STD_INPUT_HANDLE)
        mode = wintypes.DWORD()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            new_mode = mode.value | ENABLE_VIRTUAL_TERMINAL_INPUT
            kernel32.SetConsoleMode(handle, new_mode)
            return True
        return False
    except Exception:
        return False
