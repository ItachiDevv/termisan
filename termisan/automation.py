"""Multi-pane automation for Termisan.

Supports launching multiple themed sessions via:
- Ghostty (native splits + AppleScript on macOS)
- tmux (cross-platform fallback)
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from termisan.platform import IS_MACOS, IS_WINDOWS
from termisan.themes import ALL_THEMES


def launch_multi_session(
    theme_ids: list[str],
    command: str | None = None,
    extra_args: list[str] | None = None,
) -> None:
    """Launch multiple Termisan sessions in split panes.

    Automatically picks the best method:
    1. Ghostty (if installed) — AppleScript on macOS, separate windows elsewhere
    2. tmux (if installed) — split panes in a tmux session
    3. Separate terminal windows (fallback)

    Args:
        theme_ids: List of theme IDs to launch.
        command: Command to wrap in each pane.
        extra_args: Extra arguments for the wrapped command.
    """
    from rich.console import Console
    console = Console()

    # Validate themes
    for tid in theme_ids:
        if tid not in ALL_THEMES:
            console.print(f"[red]Unknown theme '{tid}'.[/]")
            console.print(f"Available: {', '.join(ALL_THEMES.keys())}")
            return

    if len(theme_ids) < 2:
        console.print("[red]--multi requires at least 2 themes.[/]")
        return

    # Build the termisan command for each pane
    cmds = []
    for tid in theme_ids:
        parts = [sys.executable, "-m", "termisan", "-t", tid]
        if command:
            parts.extend(["-c", command])
        if extra_args:
            parts.append("--")
            parts.extend(extra_args)
        cmds.append(parts)

    # Try Ghostty first (macOS AppleScript), then tmux, then fallback
    if IS_MACOS and shutil.which("ghostty") and _try_ghostty_applescript(cmds, theme_ids, console):
        return

    if shutil.which("tmux") and _try_tmux(cmds, theme_ids, console):
        return

    if shutil.which("ghostty"):
        _launch_separate_windows_ghostty(cmds, theme_ids, console)
        return

    _launch_separate_processes(cmds, theme_ids, console)


def _try_ghostty_applescript(
    cmds: list[list[str]], theme_ids: list[str], console
) -> bool:
    """Launch via Ghostty AppleScript (macOS only).

    Creates splits in a single Ghostty window.
    Returns True on success.
    """
    # Build the shell commands as strings
    shell_cmds = [" ".join(_quote_args(cmd)) for cmd in cmds]

    # Build AppleScript
    script_lines = [
        'tell application "Ghostty"',
        "    activate",
        "    delay 0.5",
        "    tell front window",
        "        tell front tab",
        "            tell front terminal",
        f'                write "{_escape_applescript(shell_cmds[0])}"',
        "            end tell",
        "        end tell",
    ]

    # For each additional session, create a split
    for i, shell_cmd in enumerate(shell_cmds[1:], 1):
        # Alternate between horizontal and vertical splits
        script_lines.extend([
            "        -- Create split for session " + str(i + 1),
            '        tell application "System Events"',
            '            tell process "Ghostty"',
        ])
        if i % 2 == 1:
            # Split right
            script_lines.append(
                '                keystroke "d" using {command down}'
            )
        else:
            # Split down
            script_lines.append(
                '                keystroke "d" using {command down, shift down}'
            )
        script_lines.extend([
            "            end tell",
            "        end tell",
            "        delay 0.3",
            "        tell front tab",
            "            tell front terminal",
            f'                write "{_escape_applescript(shell_cmd)}"',
            "            end tell",
            "        end tell",
        ])

    script_lines.extend([
        "    end tell",
        "end tell",
    ])

    script = "\n".join(script_lines)

    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            names = [ALL_THEMES[tid].name for tid in theme_ids]
            console.print(
                f"[bold green]Launched {len(theme_ids)} sessions in Ghostty:[/] "
                + ", ".join(names)
            )
            return True
        # AppleScript failed — fall through to other methods
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _try_tmux(
    cmds: list[list[str]], theme_ids: list[str], console
) -> bool:
    """Launch via tmux split panes.

    Creates a new tmux session with splits for each theme.
    Returns True on success.
    """
    session_name = "termisan-multi"

    # Kill existing session if present
    subprocess.run(
        ["tmux", "kill-session", "-t", session_name],
        capture_output=True,
    )

    shell_cmds = [" ".join(_quote_args(cmd)) for cmd in cmds]

    # Create session with first pane
    result = subprocess.run(
        ["tmux", "new-session", "-d", "-s", session_name, "-x", "200", "-y", "50"],
        capture_output=True,
    )
    if result.returncode != 0:
        return False

    # Send first command
    subprocess.run(
        ["tmux", "send-keys", "-t", session_name, shell_cmds[0], "Enter"],
        capture_output=True,
    )

    # Create splits for remaining commands
    for i, shell_cmd in enumerate(shell_cmds[1:], 1):
        # Alternate horizontal/vertical splits
        split_flag = "-h" if i % 2 == 1 else "-v"
        subprocess.run(
            ["tmux", "split-window", split_flag, "-t", session_name],
            capture_output=True,
        )
        subprocess.run(
            ["tmux", "send-keys", "-t", session_name, shell_cmd, "Enter"],
            capture_output=True,
        )

    # Equalize pane sizes
    subprocess.run(
        ["tmux", "select-layout", "-t", session_name, "tiled"],
        capture_output=True,
    )

    # Attach to the session
    names = [ALL_THEMES[tid].name for tid in theme_ids]
    console.print(
        f"[bold green]Launching {len(theme_ids)} sessions in tmux:[/] "
        + ", ".join(names)
    )
    console.print("[dim]Detach with Ctrl+B D, reattach with: tmux attach -t termisan-multi[/]")

    os.execvp("tmux", ["tmux", "attach", "-t", session_name])
    # execvp replaces the process, so we won't reach here
    return True


def _launch_separate_windows_ghostty(
    cmds: list[list[str]], theme_ids: list[str], console
) -> None:
    """Launch each session in a separate Ghostty window."""
    for i, (cmd, tid) in enumerate(zip(cmds, theme_ids)):
        shell_cmd = " ".join(_quote_args(cmd))
        subprocess.Popen(
            ["ghostty", "-e", "sh", "-c", shell_cmd],
            start_new_session=True,
        )

    names = [ALL_THEMES[tid].name for tid in theme_ids]
    console.print(
        f"[bold green]Launched {len(theme_ids)} Ghostty windows:[/] "
        + ", ".join(names)
    )


def _launch_separate_processes(
    cmds: list[list[str]], theme_ids: list[str], console
) -> None:
    """Fallback: launch each session as a background process."""
    console.print(
        "[yellow]No Ghostty or tmux found. Launching sessions as separate processes.[/]"
    )
    console.print("[dim]Each session will run in the background.[/]")
    console.print()

    for cmd, tid in zip(cmds, theme_ids):
        name = ALL_THEMES[tid].name
        proc = subprocess.Popen(
            cmd,
            start_new_session=True,
        )
        console.print(f"  [green]Started[/] {name} (PID {proc.pid})")

    console.print()
    console.print(f"[bold]Launched {len(theme_ids)} sessions.[/]")


def _quote_args(args: list[str]) -> list[str]:
    """Shell-quote arguments that need it."""
    import shlex
    return [shlex.quote(a) for a in args]


def _escape_applescript(s: str) -> str:
    """Escape a string for use inside AppleScript double quotes."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def generate_tmux_script(
    theme_ids: list[str],
    command: str | None = None,
    extra_args: list[str] | None = None,
) -> str:
    """Generate a shell script for creating a tmux multi-pane workspace.

    Can be saved to a file and run later.
    """
    session_name = "termisan-multi"

    lines = [
        "#!/bin/bash",
        f"# Termisan multi-agent workspace ({len(theme_ids)} sessions)",
        f"# Themes: {', '.join(theme_ids)}",
        "",
        f'SESSION="{session_name}"',
        "",
        "# Kill existing session if present",
        'tmux kill-session -t "$SESSION" 2>/dev/null',
        "",
    ]

    for i, tid in enumerate(theme_ids):
        parts = ["termisan", "-t", tid]
        if command:
            parts.extend(["-c", command])
        if extra_args:
            parts.append("--")
            parts.extend(extra_args)
        cmd_str = " ".join(parts)

        if i == 0:
            lines.extend([
                "# Create session with first pane",
                f'tmux new-session -d -s "$SESSION" -x 200 -y 50',
                f'tmux send-keys -t "$SESSION" \'{cmd_str}\' Enter',
                "",
            ])
        else:
            split_flag = "-h" if i % 2 == 1 else "-v"
            lines.extend([
                f"# Pane {i + 1}: {ALL_THEMES[tid].name}",
                f'tmux split-window {split_flag} -t "$SESSION"',
                f'tmux send-keys -t "$SESSION" \'{cmd_str}\' Enter',
                "",
            ])

    lines.extend([
        "# Equalize panes and attach",
        'tmux select-layout -t "$SESSION" tiled',
        'tmux attach -t "$SESSION"',
        "",
    ])

    return "\n".join(lines)
