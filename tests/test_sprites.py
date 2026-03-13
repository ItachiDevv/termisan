"""Tests for sprite art."""

from termisan.sprites import get_sprite, get_sprite_lines, get_sprite_dimensions
from termisan.themes import ALL_THEMES


def test_all_themes_have_sprites():
    for theme_id in ALL_THEMES:
        sprite = get_sprite(theme_id)
        assert sprite, f"No sprite for theme '{theme_id}'"


def test_sprite_lines_not_empty():
    for theme_id in ALL_THEMES:
        lines = get_sprite_lines(theme_id)
        assert len(lines) > 0, f"Empty sprite lines for '{theme_id}'"


def test_sprite_dimensions_reasonable():
    for theme_id in ALL_THEMES:
        height, width = get_sprite_dimensions(theme_id)
        assert height >= 5, f"Sprite too short for '{theme_id}': {height}"
        assert width >= 10, f"Sprite too narrow for '{theme_id}': {width}"
        assert height <= 30, f"Sprite too tall for '{theme_id}': {height}"
        assert width <= 60, f"Sprite too wide for '{theme_id}': {width}"


def test_unknown_theme_returns_fallback():
    sprite = get_sprite("nonexistent_theme_xyz")
    # Should return empty string or a fallback, not crash
    assert isinstance(sprite, str)
