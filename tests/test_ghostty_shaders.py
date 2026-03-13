"""Tests for Ghostty GLSL shader generation."""

import tempfile
from pathlib import Path

from termisan.ghostty_shaders import (
    SHADER_GENERATORS,
    generate_shader,
    install_shader,
    install_all_shaders,
)
from termisan.themes import ALL_THEMES


def test_all_themes_have_shaders():
    """Every theme should have a shader generator."""
    for theme_id in ALL_THEMES:
        assert theme_id in SHADER_GENERATORS, f"No shader for theme '{theme_id}'"


def test_generate_shader_returns_glsl():
    for theme_id in ALL_THEMES:
        shader = generate_shader(theme_id)
        assert shader is not None, f"generate_shader returned None for '{theme_id}'"
        assert "void mainImage" in shader, f"Shader for '{theme_id}' missing mainImage"
        assert "fragColor" in shader, f"Shader for '{theme_id}' missing fragColor"
        assert "iChannel0" in shader, f"Shader for '{theme_id}' missing iChannel0"


def test_generate_shader_unknown_theme():
    result = generate_shader("nonexistent_xyz")
    assert result is None


def test_shader_has_theme_name():
    for theme_id in ALL_THEMES:
        shader = generate_shader(theme_id)
        theme_name = ALL_THEMES[theme_id].name
        assert theme_name in shader, f"Shader for '{theme_id}' doesn't mention theme name"


def test_install_shader_writes_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        path = install_shader("naruto", config_dir=config_dir)

        assert path is not None
        assert path.exists()
        assert path.name == "termisan-naruto.glsl"
        content = path.read_text()
        assert "void mainImage" in content


def test_install_shader_unknown_theme():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = install_shader("nonexistent_xyz", config_dir=Path(tmpdir))
        assert result is None


def test_install_all_shaders():
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir)
        paths = install_all_shaders(config_dir=config_dir)

        assert len(paths) == 20
        for p in paths:
            assert p.exists()
            assert p.suffix == ".glsl"


def test_shader_valid_glsl_syntax():
    """Basic syntax validation — braces are balanced."""
    for theme_id in ALL_THEMES:
        shader = generate_shader(theme_id)
        open_braces = shader.count("{")
        close_braces = shader.count("}")
        assert open_braces == close_braces, (
            f"Unbalanced braces in shader for '{theme_id}': "
            f"{open_braces} open, {close_braces} close"
        )
