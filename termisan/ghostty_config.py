"""Ghostty configuration generator for Termisan themes.

Generates complete Ghostty config files from Termisan's AnimeTheme
definitions. Each theme maps its hex colors to Ghostty's color settings,
and optionally references a matching GLSL shader.
"""

import sys
from pathlib import Path

from termisan.themes import ALL_THEMES, AnimeTheme


def _rich_color_to_hex(color: str) -> str:
    """Convert a Rich color name or hex string to a bare hex value.

    Rich uses names like 'bright_red' or hex like '#FF0000'.
    Ghostty config needs bare hex: FF0000 or named CSS colors.
    """
    # Already hex
    if color.startswith("#"):
        return color.lstrip("#")

    # Map common Rich names to hex
    RICH_TO_HEX = {
        "black": "000000",
        "red": "CC0000",
        "green": "00CC00",
        "yellow": "CCCC00",
        "blue": "0000CC",
        "magenta": "CC00CC",
        "cyan": "00CCCC",
        "white": "CCCCCC",
        "bright_black": "666666",
        "bright_red": "FF0000",
        "bright_green": "00FF00",
        "bright_yellow": "FFFF00",
        "bright_blue": "0000FF",
        "bright_magenta": "FF00FF",
        "bright_cyan": "00FFFF",
        "bright_white": "FFFFFF",
    }
    return RICH_TO_HEX.get(color, color)


def generate_ghostty_config(theme: AnimeTheme, include_shader: bool = True) -> str:
    """Generate a Ghostty config string for the given theme.

    Args:
        theme: The AnimeTheme to convert.
        include_shader: Whether to include the shader reference.

    Returns:
        A Ghostty config file as a string.
    """
    bg = _rich_color_to_hex(theme.color_bg)
    fg = _rich_color_to_hex(theme.color_text)
    primary = _rich_color_to_hex(theme.color_primary)
    secondary = _rich_color_to_hex(theme.color_secondary)
    accent = _rich_color_to_hex(theme.color_accent)

    lines = [
        f"# Termisan Theme: {theme.name}",
        f"# {theme.description}",
        f"# {theme.year} | {theme.genre}",
        "",
        "# Colors",
        f"background = {bg}",
        f"foreground = {fg}",
        f"cursor-color = {primary}",
        f"cursor-text = {bg}",
        f"selection-background = {secondary}",
        f"selection-foreground = {bg}",
        "",
        "# ANSI palette — normal",
        f"palette = 0={bg}",
        f"palette = 1={primary}",
        f"palette = 2={accent}",
        f"palette = 3={secondary}",
        f"palette = 4={_rich_color_to_hex(theme.color_accent)}",
        f"palette = 5={primary}",
        f"palette = 6={secondary}",
        f"palette = 7={fg}",
        "",
        "# ANSI palette — bright",
        f"palette = 8=666666",
        f"palette = 9={primary}",
        f"palette = 10={accent}",
        f"palette = 11={secondary}",
        f"palette = 12={accent}",
        f"palette = 13={primary}",
        f"palette = 14={secondary}",
        f"palette = 15=FFFFFF",
        "",
        "# Window",
        f"title = {theme.prompt_icon} Termisan: {theme.name} {theme.prompt_icon}",
        "background-opacity = 0.95",
        "background-blur-radius = 20",
        "",
        "# Font",
        "font-family = JetBrains Mono Nerd Font",
        "font-size = 14",
        "",
        "# Padding",
        "window-padding-x = 8",
        "window-padding-y = 4",
    ]

    if include_shader:
        lines.extend([
            "",
            "# Termisan shader",
            f"custom-shader = ~/.config/ghostty/shaders/termisan-{theme.id}.glsl",
            "custom-shader-animation = true",
        ])

    lines.append("")
    return "\n".join(lines)


def write_ghostty_config(
    theme_id: str,
    output_path: Path | None = None,
    include_shader: bool = True,
) -> Path | None:
    """Write a Ghostty config file for the given theme.

    Args:
        theme_id: Theme ID to generate config for.
        output_path: Where to write. Defaults to
                      ~/.config/ghostty/termisan-<theme_id>.conf
        include_shader: Whether to include shader reference.

    Returns:
        Path to the written file, or None if theme not found.
    """
    if theme_id not in ALL_THEMES:
        return None

    theme = ALL_THEMES[theme_id]
    config = generate_ghostty_config(theme, include_shader=include_shader)

    if output_path is None:
        config_dir = Path.home() / ".config" / "ghostty"
        config_dir.mkdir(parents=True, exist_ok=True)
        output_path = config_dir / f"termisan-{theme_id}.conf"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(config)
    return output_path


def print_ghostty_config(theme_id: str, include_shader: bool = True) -> bool:
    """Print a Ghostty config to stdout.

    Returns True on success, False if theme not found.
    """
    if theme_id not in ALL_THEMES:
        print(f"Error: Unknown theme '{theme_id}'.", file=sys.stderr)
        print(f"Available: {', '.join(ALL_THEMES.keys())}", file=sys.stderr)
        return False

    theme = ALL_THEMES[theme_id]
    config = generate_ghostty_config(theme, include_shader=include_shader)
    print(config)
    return True
