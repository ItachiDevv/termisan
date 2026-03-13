"""Tests for the terminal wrapper base class."""

from termisan.themes import ALL_THEMES
from termisan.wrapper import (
    ThemedTerminalWrapper,
    _ansi_color_bg,
    _ansi_color_fg,
    _ansi_move,
    _ansi_reset,
    _ansi_set_scroll_region,
)


def test_ansi_move():
    assert _ansi_move(1, 1) == "\033[1;1H"
    assert _ansi_move(10, 20) == "\033[10;20H"


def test_ansi_color_fg():
    result = _ansi_color_fg("#FF0000")
    assert "38;2;255;0;0" in result


def test_ansi_color_bg():
    result = _ansi_color_bg("#00FF00")
    assert "48;2;0;255;0" in result


def test_ansi_reset():
    assert _ansi_reset() == "\033[0m"


def test_ansi_set_scroll_region():
    result = _ansi_set_scroll_region(4, 20)
    assert "4;20" in result


def test_wrapper_content_area():
    theme = ALL_THEMES["naruto"]
    wrapper = ThemedTerminalWrapper(theme, ["echo", "test"])
    assert wrapper.content_top == 4  # HEADER_HEIGHT + 1
    assert wrapper.content_bottom == 23  # default rows(24) - FOOTER_HEIGHT(1)


def test_wrapper_render_header():
    theme = ALL_THEMES["dragonball"]
    wrapper = ThemedTerminalWrapper(theme, ["echo"])
    wrapper.rows = 24
    wrapper.cols = 80
    header = wrapper._render_header()
    assert "Dragon Ball Z" in header


def test_wrapper_render_footer():
    theme = ALL_THEMES["deathnote"]
    wrapper = ThemedTerminalWrapper(theme, ["echo"])
    wrapper.rows = 24
    wrapper.cols = 80
    footer = wrapper._render_footer()
    assert "TERMISAN" in footer


def test_wrapper_run_not_implemented():
    theme = ALL_THEMES["naruto"]
    wrapper = ThemedTerminalWrapper(theme, ["echo"])
    try:
        wrapper.run()
        assert False, "Should have raised NotImplementedError"
    except NotImplementedError:
        pass
