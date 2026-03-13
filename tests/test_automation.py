"""Tests for multi-pane automation."""

from termisan.automation import generate_tmux_script, _quote_args, _escape_applescript
from termisan.themes import ALL_THEMES


def test_generate_tmux_script_basic():
    script = generate_tmux_script(["naruto", "dragonball"])
    assert "#!/bin/bash" in script
    assert "tmux new-session" in script
    assert "naruto" in script
    assert "dragonball" in script
    assert "tmux select-layout" in script


def test_generate_tmux_script_with_command():
    script = generate_tmux_script(["naruto", "dragonball"], command="claude")
    assert "-c claude" in script


def test_generate_tmux_script_with_extra_args():
    script = generate_tmux_script(
        ["naruto", "dragonball"],
        command="claude",
        extra_args=["--model", "opus"],
    )
    assert "--model" in script
    assert "opus" in script


def test_generate_tmux_script_alternates_splits():
    script = generate_tmux_script(["naruto", "dragonball", "deathnote"])
    assert "-h" in script  # First split is horizontal
    assert "-v" in script  # Second split is vertical


def test_generate_tmux_script_three_themes():
    script = generate_tmux_script(["naruto", "dragonball", "deathnote"])
    assert "naruto" in script
    assert "dragonball" in script
    assert "deathnote" in script
    assert script.count("tmux send-keys") == 3


def test_quote_args():
    result = _quote_args(["python", "-m", "termisan", "--theme", "naruto"])
    assert all(isinstance(r, str) for r in result)


def test_escape_applescript():
    result = _escape_applescript('say "hello"')
    assert '\\"' in result
    assert "\\\\" not in result  # No backslashes in input

    result2 = _escape_applescript("path\\to\\file")
    assert "\\\\" in result2
