"""Tests for platform detection."""

import sys

from termisan.platform import (
    IS_LINUX,
    IS_MACOS,
    IS_UNIX,
    IS_WINDOWS,
    get_terminal_size,
)


def test_platform_flags_are_booleans():
    assert isinstance(IS_WINDOWS, bool)
    assert isinstance(IS_MACOS, bool)
    assert isinstance(IS_LINUX, bool)
    assert isinstance(IS_UNIX, bool)


def test_platform_flags_consistent():
    """At least one platform flag should be True."""
    assert IS_WINDOWS or IS_MACOS or IS_LINUX


def test_unix_includes_linux_and_macos():
    if IS_LINUX or IS_MACOS:
        assert IS_UNIX


def test_windows_is_not_unix():
    if IS_WINDOWS:
        assert not IS_UNIX


def test_get_terminal_size_returns_tuple():
    rows, cols = get_terminal_size()
    assert isinstance(rows, int)
    assert isinstance(cols, int)
    assert rows > 0
    assert cols > 0
