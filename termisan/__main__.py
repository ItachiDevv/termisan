"""Entry point for Termisan - Anime-themed terminal wrapper."""

import argparse
import sys

from termisan import __version__
from termisan.themes import ALL_THEMES


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="termisan",
        description="Anime-themed terminal wrapper for Claude and Codex sessions",
        epilog="Transform your coding sessions into an anime experience!",
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"termisan {__version__}",
    )

    parser.add_argument(
        "-t", "--theme",
        choices=list(ALL_THEMES.keys()),
        help="Pre-select an anime theme (skip selection menu)",
        metavar="THEME",
    )

    parser.add_argument(
        "-c", "--command",
        help="Command to wrap (default: auto-detect claude or codex)",
        metavar="CMD",
    )

    parser.add_argument(
        "-l", "--list-themes",
        action="store_true",
        help="List all available themes and exit",
    )

    parser.add_argument(
        "-p", "--preview",
        metavar="THEME",
        help="Preview a theme and exit",
    )

    parser.add_argument(
        "extra_args",
        nargs="*",
        help="Additional arguments to pass to the wrapped command",
    )

    return parser.parse_args()


def list_themes() -> None:
    """Print all available themes."""
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(
        title="Available Termisan Themes",
        title_style="bold bright_magenta",
        border_style="bright_magenta",
    )
    table.add_column("#", style="bold", width=3)
    table.add_column("ID", style="cyan", min_width=12)
    table.add_column("Name", style="bold white", min_width=25)
    table.add_column("Category", style="yellow", width=10)
    table.add_column("Genre", style="dim", min_width=15)
    table.add_column("Year", style="dim cyan", width=12)

    for i, (tid, theme) in enumerate(ALL_THEMES.items(), 1):
        cat_label = "Classic" if theme.category == "classic" else "Modern"
        table.add_row(str(i), tid, theme.name, cat_label, theme.genre, theme.year)

    console.print(table)


def preview_theme(theme_id: str) -> None:
    """Preview a specific theme."""
    from rich.console import Console
    from termisan.selector import show_theme_preview

    if theme_id not in ALL_THEMES:
        print(f"Error: Unknown theme '{theme_id}'.")
        print(f"Available themes: {', '.join(ALL_THEMES.keys())}")
        sys.exit(1)

    console = Console()
    show_theme_preview(console, ALL_THEMES[theme_id])


def main() -> None:
    """Main entry point."""
    args = parse_args()

    if args.list_themes:
        list_themes()
        sys.exit(0)

    if args.preview:
        preview_theme(args.preview)
        sys.exit(0)

    from termisan.app import run_app

    exit_code = run_app(
        theme_id=args.theme,
        command=args.command,
        extra_args=args.extra_args if args.extra_args else None,
    )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
