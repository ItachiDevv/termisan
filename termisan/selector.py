"""Anime theme selection menu using Rich."""

import random
import sys

from rich.align import Align
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from termisan.sprites import get_sprite_lines
from termisan.themes import ALL_THEMES, CLASSIC_THEMES, MODERN_THEMES, AnimeTheme

TERMISAN_LOGO = r"""
 ████████╗███████╗██████╗ ███╗   ███╗██╗███████╗ █████╗ ███╗   ██╗
 ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔════╝██╔══██╗████╗  ██║
    ██║   █████╗  ██████╔╝██╔████╔██║██║███████╗███████║██╔██╗ ██║
    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║╚════██║██╔══██║██║╚██╗██║
    ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║███████║██║  ██║██║ ╚████║
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝
"""

TERMISAN_LOGO_SMALL = r"""
╔╦╗┌─┐┬─┐┌┬┐┬┌─┐┌─┐┌┐┌
 ║ ├┤ ├┬┘│││││└─┐├─┤│││
 ╩ └─┘┴└─┘ ┘┴└─┘┴ ┴┘└┘
"""


def show_selection_menu(console: Console) -> AnimeTheme | None:
    """Display the anime theme selection menu and return the chosen theme."""
    console.clear()

    # Show logo
    width = console.width
    if width >= 75:
        logo = TERMISAN_LOGO
    else:
        logo = TERMISAN_LOGO_SMALL

    console.print(
        Align.center(
            Text(logo, style="bold bright_magenta")
        )
    )
    console.print(
        Align.center(
            Text(
                "~ Anime-Themed Terminal Wrapper ~",
                style="italic bright_cyan",
            )
        )
    )
    console.print(
        Align.center(
            Text(
                "Transform your Claude & Codex sessions into an anime experience!",
                style="dim white",
            )
        )
    )
    console.print()

    # Build the two category tables
    classic_table = _build_theme_table(
        "🏆 All-Time Classics",
        CLASSIC_THEMES,
        "bright_yellow",
        start_num=1,
    )
    modern_table = _build_theme_table(
        "🔥 Modern Hits (2019-2026)",
        MODERN_THEMES,
        "bright_cyan",
        start_num=11,
    )

    # Display side-by-side if terminal is wide enough, otherwise stacked
    if width >= 100:
        console.print(Columns([classic_table, modern_table], padding=(0, 2)))
    else:
        console.print(classic_table)
        console.print()
        console.print(modern_table)

    console.print()

    # Special options
    console.print(
        Align.center(
            Text("  [R] Random  |  [Q] Quit  ", style="bold bright_white on dark_red")
        )
    )
    console.print()

    # Get user choice
    theme = _get_user_choice(console)
    return theme


def _build_theme_table(
    title: str,
    themes: dict[str, AnimeTheme],
    title_style: str,
    start_num: int,
) -> Table:
    """Build a Rich table for a theme category."""
    table = Table(
        title=title,
        title_style=f"bold {title_style}",
        border_style=title_style,
        show_header=True,
        header_style=f"bold {title_style}",
        padding=(0, 1),
        expand=False,
    )
    table.add_column("#", style="bold white", width=3, justify="right")
    table.add_column("Anime", style="bold bright_white", min_width=20)
    table.add_column("Genre", style="dim", min_width=12)
    table.add_column("Year", style="dim cyan", width=12)

    for i, (theme_id, theme) in enumerate(themes.items(), start=start_num):
        table.add_row(
            str(i),
            theme.name,
            theme.genre,
            theme.year,
        )

    return table


def _get_user_choice(console: Console) -> AnimeTheme | None:
    """Prompt the user to pick a theme by number."""
    theme_list = list(ALL_THEMES.values())

    while True:
        try:
            choice = console.input(
                "[bold bright_magenta]Choose your anime (1-20, R, or Q): [/]"
            ).strip().upper()
        except (EOFError, KeyboardInterrupt):
            return None

        if choice == "Q":
            return None

        if choice == "R":
            theme = random.choice(theme_list)
            console.print(
                f"[bold bright_yellow]🎲 Randomly selected: {theme.name}![/]"
            )
            return theme

        try:
            num = int(choice)
            if 1 <= num <= 20:
                theme = theme_list[num - 1]
                return theme
            else:
                console.print("[red]Please enter a number between 1 and 20.[/]")
        except ValueError:
            # Check if they typed a theme name/id
            for theme in theme_list:
                if (
                    choice.lower() == theme.id.lower()
                    or choice.lower() == theme.name.lower()
                ):
                    return theme
            console.print("[red]Invalid choice. Enter a number, R, or Q.[/]")


def show_theme_preview(console: Console, theme: AnimeTheme) -> None:
    """Show a full preview of the selected theme before launching."""
    console.clear()

    # Get sprite lines
    sprite_lines = get_sprite_lines(theme.id)
    sprite_text = "\n".join(sprite_lines)

    # Build the sprite panel
    sprite_panel = Panel(
        Align.center(Text(sprite_text, style=f"bold {theme.color_primary}")),
        border_style=theme.color_primary,
        title=f"[bold {theme.color_secondary}]{theme.prompt_icon} {theme.name} {theme.prompt_icon}[/]",
        subtitle=f"[dim]{theme.year} | {theme.genre}[/]",
        padding=(1, 2),
    )

    # Build the info panel
    quote = random.choice(theme.quotes) if theme.quotes else ""
    info_text = Text()
    info_text.append(f"\n  {theme.description}\n\n", style=theme.color_text)
    info_text.append(f'  "{quote}"\n\n', style=f"italic {theme.color_secondary}")
    info_text.append(f"  {theme.welcome}\n", style=f"bold {theme.color_accent}")

    info_panel = Panel(
        info_text,
        border_style=theme.color_secondary,
        title=f"[bold {theme.color_primary}]Theme Info[/]",
        padding=(0, 1),
    )

    # Display
    console.print()
    if console.width >= 80:
        console.print(Columns([sprite_panel, info_panel], padding=(0, 2)))
    else:
        console.print(sprite_panel)
        console.print(info_panel)

    console.print()
    console.print(
        Align.center(
            Text(
                f"  {theme.status_left}  |  {theme.status_right}  ",
                style=f"bold bright_white on {theme.color_primary}",
            )
        )
    )
    console.print()
