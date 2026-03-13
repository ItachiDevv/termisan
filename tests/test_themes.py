"""Tests for theme definitions."""

from termisan.themes import ALL_THEMES, CLASSIC_THEMES, MODERN_THEMES, AnimeTheme


def test_total_theme_count():
    assert len(ALL_THEMES) == 20


def test_classic_themes_count():
    assert len(CLASSIC_THEMES) == 10


def test_modern_themes_count():
    assert len(MODERN_THEMES) == 10


def test_all_themes_have_required_fields():
    for theme_id, theme in ALL_THEMES.items():
        assert isinstance(theme, AnimeTheme)
        assert theme.id == theme_id
        assert theme.name
        assert theme.category in ("classic", "modern")
        assert theme.year
        assert theme.genre
        assert theme.description
        assert theme.color_primary
        assert theme.color_secondary
        assert theme.color_accent
        assert theme.color_bg
        assert theme.color_text
        assert theme.border_style
        assert theme.border_color
        assert theme.prompt_icon
        assert theme.prompt_style


def test_all_themes_have_quotes():
    for theme_id, theme in ALL_THEMES.items():
        assert len(theme.quotes) >= 1, f"{theme_id} has no quotes"


def test_all_themes_have_welcome():
    for theme_id, theme in ALL_THEMES.items():
        assert theme.welcome, f"{theme_id} has no welcome message"


def test_all_themes_have_status():
    for theme_id, theme in ALL_THEMES.items():
        assert theme.status_left, f"{theme_id} has no status_left"
        assert theme.status_right, f"{theme_id} has no status_right"


def test_theme_ids_are_unique():
    ids = [t.id for t in ALL_THEMES.values()]
    assert len(ids) == len(set(ids))


def test_hex_colors_valid():
    """All hex color values should be valid #RRGGBB format."""
    for theme_id, theme in ALL_THEMES.items():
        for field_name in ("color_primary", "color_secondary", "color_accent", "color_bg", "color_text"):
            color = getattr(theme, field_name)
            if color.startswith("#"):
                assert len(color) == 7, f"{theme_id}.{field_name} = {color} is not #RRGGBB"
                int(color[1:], 16)  # Should not raise
