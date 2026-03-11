"""Main application orchestration for Termisan."""

import shutil
import sys

from rich.console import Console

from termisan.selector import show_selection_menu, show_theme_preview
from termisan.themes import ALL_THEMES, AnimeTheme
from termisan.wrapper import run_wrapped_session


def detect_available_commands() -> list[str]:
    """Detect which AI CLI tools are available on the system."""
    commands = []
    for cmd in ["claude", "codex"]:
        if shutil.which(cmd):
            commands.append(cmd)
    return commands


def choose_command(console: Console, available: list[str]) -> str | None:
    """Let the user choose which command to wrap."""
    if not available:
        console.print(
            "[bold red]Error:[/] Neither 'claude' nor 'codex' found in PATH.\n"
            "Please install one of them first:\n"
            "  - Claude: [cyan]npm install -g @anthropic-ai/claude-code[/]\n"
            "  - Codex: [cyan]npm install -g @openai/codex[/]\n"
        )
        return None

    if len(available) == 1:
        return available[0]

    console.print()
    console.print("[bold bright_magenta]Which AI assistant do you want to wrap?[/]")
    for i, cmd in enumerate(available, 1):
        console.print(f"  [bold]{i}[/]. {cmd}")
    console.print()

    while True:
        try:
            choice = console.input("[bold]Choose (1-2): [/]").strip()
        except (EOFError, KeyboardInterrupt):
            return None
        try:
            idx = int(choice)
            if 1 <= idx <= len(available):
                return available[idx - 1]
        except ValueError:
            if choice.lower() in available:
                return choice.lower()
        console.print("[red]Invalid choice.[/]")


def run_app(
    theme_id: str | None = None,
    command: str | None = None,
    extra_args: list[str] | None = None,
) -> int:
    """Run the Termisan application.

    Args:
        theme_id: Pre-selected theme ID (skip selection menu if provided).
        command: Pre-selected command to wrap (skip detection if provided).
        extra_args: Extra arguments to pass to the wrapped command.

    Returns:
        Exit code.
    """
    console = Console()

    # Select theme
    if theme_id and theme_id in ALL_THEMES:
        theme = ALL_THEMES[theme_id]
    else:
        theme = show_selection_menu(console)
        if theme is None:
            console.print("[dim]Sayonara![/]")
            return 0

    # Show theme preview
    show_theme_preview(console, theme)

    # Detect or use provided command
    if command:
        cmd = command
    else:
        available = detect_available_commands()
        cmd = choose_command(console, available)
        if cmd is None:
            return 1

    # Build full command
    full_command = [cmd]
    if extra_args:
        full_command.extend(extra_args)

    # Confirmation
    console.print()
    console.print(
        f"[bold {theme.color_primary}]Launching [bright_white]{cmd}[/bright_white] "
        f"with [bright_white]{theme.name}[/bright_white] theme...[/]"
    )
    console.print()

    try:
        console.input("[dim]Press Enter to start (or Ctrl+C to cancel)...[/]")
    except (EOFError, KeyboardInterrupt):
        console.print("\n[dim]Cancelled.[/]")
        return 0

    # Launch wrapped session
    return run_wrapped_session(theme, full_command)
