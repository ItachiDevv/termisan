"""Tests for Ghostty config generation."""

import tempfile
from pathlib import Path

from termisan.ghostty_config import (
    generate_ghostty_config,
    write_ghostty_config,
)
from termisan.themes import ALL_THEMES


def test_generate_config_for_all_themes():
    for theme_id, theme in ALL_THEMES.items():
        config = generate_ghostty_config(theme)
        assert "background =" in config
        assert "foreground =" in config
        assert "cursor-color =" in config
        assert "font-family =" in config
        assert theme.name in config


def test_config_includes_shader_by_default():
    theme = ALL_THEMES["dragonball"]
    config = generate_ghostty_config(theme, include_shader=True)
    assert "custom-shader =" in config
    assert "termisan-dragonball.glsl" in config
    assert "custom-shader-animation = true" in config


def test_config_excludes_shader_when_disabled():
    theme = ALL_THEMES["dragonball"]
    config = generate_ghostty_config(theme, include_shader=False)
    assert "custom-shader" not in config


def test_config_has_palette():
    theme = ALL_THEMES["naruto"]
    config = generate_ghostty_config(theme)
    assert "palette = 0=" in config
    assert "palette = 15=" in config


def test_config_has_window_title():
    theme = ALL_THEMES["deathnote"]
    config = generate_ghostty_config(theme)
    assert "title =" in config
    assert "Death Note" in config


def test_write_config_creates_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.conf"
        result = write_ghostty_config("naruto", output_path=output_path)

        assert result is not None
        assert result.exists()
        content = result.read_text()
        assert "Naruto" in content


def test_write_config_unknown_theme():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = write_ghostty_config(
            "nonexistent_xyz",
            output_path=Path(tmpdir) / "test.conf",
        )
        assert result is None


def test_write_config_default_path():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Override home to use temp dir
        result = write_ghostty_config(
            "pokemon",
            output_path=Path(tmpdir) / "termisan-pokemon.conf",
        )
        assert result is not None
        assert result.name == "termisan-pokemon.conf"
