# Termisan Usage Guide

> Complete guide to using Termisan — the anime-themed terminal wrapper for Claude and Codex sessions.
> Works on **macOS**, **Linux**, and **Windows**.

---

## Table of Contents

1. [Installation](#1-installation)
2. [Quick Start](#2-quick-start)
3. [CLI Commands & Flags](#3-cli-commands--flags)
4. [Theme Selection](#4-theme-selection)
5. [Running Wrapped Sessions](#5-running-wrapped-sessions)
6. [Multi-Agent Sessions](#6-multi-agent-sessions)
7. [Ghostty Terminal Integration](#7-ghostty-terminal-integration)
8. [Platform-Specific Notes](#8-platform-specific-notes)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Installation

### Prerequisites

- **Python 3.9+**
- One or both of:
  - [Claude Code](https://docs.anthropic.com/en/docs/claude-code): `npm install -g @anthropic-ai/claude-code`
  - [Codex](https://github.com/openai/codex): `npm install -g @openai/codex`

### Install Termisan

```bash
# From source
git clone https://github.com/ItachiDevv/termisan.git
cd termisan
pip install -e .

# Or install directly
pip install .
```

### Platform Dependencies

| Platform | Auto-installed | Notes |
|----------|---------------|-------|
| **macOS** | Nothing extra | Uses native PTY (built into Python) |
| **Linux** | Nothing extra | Uses native PTY (built into Python) |
| **Windows** | `pywinpty` | ConPTY support (Windows 10 1809+) |

On Windows, `pywinpty` is automatically installed as a dependency.

---

## 2. Quick Start

```bash
# Launch with interactive theme selector
termisan

# Launch with a specific theme
termisan -t naruto

# Launch wrapping a specific command
termisan -c claude

# Launch with theme + command + extra args
termisan -t dragonball -c claude -- --model opus
```

### What Happens

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. Theme Selection Menu appears (or skipped with -t flag)           │
│ 2. Theme Preview shows sprite art + quote + description             │
│ 3. Auto-detects claude/codex in PATH (or uses -c flag)              │
│ 4. Press Enter to launch the themed session                         │
│ 5. Your AI CLI runs inside the anime-themed terminal frame          │
│ 6. Ctrl+C or exit the CLI to return to your normal terminal         │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. CLI Commands & Flags

### Full Command Reference

```
termisan [OPTIONS] [-- EXTRA_ARGS...]
```

| Flag | Short | Description | Example |
|------|-------|-------------|---------|
| `--theme THEME` | `-t` | Pre-select a theme (skip menu) | `termisan -t demonslayer` |
| `--command CMD` | `-c` | Command to wrap | `termisan -c codex` |
| `--list-themes` | `-l` | List all 20 themes and exit | `termisan -l` |
| `--preview THEME` | `-p` | Preview a theme's art and info | `termisan -p naruto` |
| `--version` | `-v` | Show version | `termisan -v` |
| `--help` | `-h` | Show help | `termisan -h` |

### Passing Arguments to the Wrapped Command

Use `--` to separate Termisan flags from arguments passed to the wrapped CLI:

```bash
# Pass --model and --verbose to claude
termisan -t onepiece -c claude -- --model opus --verbose

# Pass a project directory to codex
termisan -t pokemon -c codex -- --project ./my-app
```

### Listing Themes

```bash
$ termisan --list-themes
```

```
┏━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ # ┃ ID            ┃ Name                    ┃ Category ┃ Genre               ┃ Year       ┃
┡━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ 1 │ dragonball    │ Dragon Ball Z           │ Classic  │ Action / Martial ..│ 1989-1996  │
│ 2 │ onepiece      │ One Piece               │ Classic  │ Adventure / Pirate  │ 1999-      │
│ 3 │ naruto        │ Naruto                  │ Classic  │ Action / Ninja      │ 2002-2017  │
│ ...                                                                                       │
│20 │ cyberpunk     │ Cyberpunk: Edgerunners  │ Modern   │ Sci-Fi / Cyberpunk  │ 2022       │
└───┴───────────────┴─────────────────────────┴──────────┴─────────────────────┴────────────┘
```

### Previewing a Theme

```bash
$ termisan --preview deathnote
```

Shows the theme's ASCII sprite art, description, quote, and color scheme without launching a session.

---

## 4. Theme Selection

### Interactive Menu

When launched without `-t`, Termisan shows a full-screen selection menu:

```
 ████████╗███████╗██████╗ ███╗   ███╗██╗███████╗ █████╗ ███╗   ██╗
 ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║██╔════╝██╔══██╗████╗  ██║
    ██║   █████╗  ██████╔╝██╔████╔██║██║███████╗███████║██╔██╗ ██║
    ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║╚════██║██╔══██║██║╚██╗██║
    ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║███████║██║  ██║██║ ╚████║
    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝

                    ~ Anime-Themed Terminal Wrapper ~

  ┌───────────────────────────────┐   ┌───────────────────────────────┐
  │  🏆 All-Time Classics        │   │  🔥 Modern Hits (2019-2026)  │
  ├─────┬──────────────┬─────────┤   ├─────┬──────────────┬─────────┤
  │  1  │ Dragon Ball Z│ Action  │   │ 11  │ Demon Slayer │ Action  │
  │  2  │ One Piece    │ Advent. │   │ 12  │ Jujutsu K.   │ Action  │
  │  3  │ Naruto       │ Ninja   │   │ 13  │ My Hero Ac.  │ Super.  │
  │  4  │ Attack on T. │ Dark F. │   │ 14  │ Spy x Family │ Comedy  │
  │  5  │ Pokémon      │ Advent. │   │ 15  │ Frieren      │ Fantasy │
  │  6  │ Death Note   │ Psycho. │   │ 16  │ Oshi no Ko   │ Drama   │
  │  7  │ FMA: Broth.  │ Fantasy │   │ 17  │ Solo Leveling│ Action  │
  │  8  │ Hunter x H.  │ Advent. │   │ 18  │ Chainsaw Man │ Dark F. │
  │  9  │ Bleach       │ Action  │   │ 19  │ Apothecary D.│ Histor. │
  │ 10  │ Cowboy Bebop │ Sci-Fi  │   │ 20  │ Cyberpunk    │ Sci-Fi  │
  └─────┴──────────────┴─────────┘   └─────┴──────────────┴─────────┘

                  [R] Random  |  [Q] Quit

  Choose your anime (1-20, R, or Q): _
```

### Selection Options

| Input | Action |
|-------|--------|
| `1`–`20` | Select a theme by number |
| `R` | Random theme |
| `Q` | Quit |
| Theme name | Type a theme name (e.g., `naruto`) |
| Theme ID | Type a theme ID (e.g., `demonslayer`) |

---

## 5. Running Wrapped Sessions

### Terminal Layout

Once launched, your terminal is divided into three regions:

```
━━━━━━━━━━━━━━━━ 🐉 Dragon Ball Z 🐉 ━━━━━━━━━━━━━━━━━  ← Header (Line 1)
 Power up your code to over 9000!                         ← Welcome (Line 2)
─────────── "I am the hope of the universe!" ───────────  ← Quote (Line 3)
                                                           ┐
  $ claude                                                 │
  > Hello! I'm Claude...                                   │ Content Area
  > How can I help you today?                              │ (Scroll Region)
  ...                                                      │
                                                           ┘
 ⚡ Saiyan Mode  │  TERMISAN │ 14:30  │  Training Arc ⚡   ← Footer (Status)
```

### How It Works

| Component | Description |
|-----------|-------------|
| **Header** (3 lines) | Theme name, welcome message, and a random quote |
| **Content Area** | Your CLI session — fully interactive with scroll |
| **Footer** (1 line) | Status bar with theme info and current time |

The content area is a **VT100 scroll region** — the header and footer stay fixed while the CLI output scrolls normally inside the content area.

### Keyboard Controls

All keyboard input is passed directly to the wrapped CLI. Termisan does **not** intercept any keys. Use whatever shortcuts your CLI supports:

| Action | Keys |
|--------|------|
| Exit session | `Ctrl+C` or type `/exit` in the CLI |
| Scroll up (if terminal supports) | `Shift+PgUp` or scroll wheel |
| Scroll down | `Shift+PgDown` or scroll wheel |

### Terminal Resize

On **macOS/Linux**: Termisan handles `SIGWINCH` — the frame and content area automatically resize when you resize your terminal window.

On **Windows**: The frame redraws when resize is detected. Works best in Windows Terminal.

---

## 6. Multi-Agent Sessions

### Running Multiple Termisan Sessions

You can run multiple Termisan sessions simultaneously in separate terminal windows or tabs. Each session is independent with its own theme.

#### Method 1: Multiple Terminal Windows

Open several terminal windows and launch Termisan in each:

```bash
# Window 1 — Claude with Naruto theme
termisan -t naruto -c claude

# Window 2 — Codex with Dragon Ball theme
termisan -t dragonball -c codex

# Window 3 — Claude with a different project
termisan -t deathnote -c claude -- --project ./backend
```

#### Method 2: Terminal Multiplexer (tmux)

```bash
# Create a new tmux session with multiple panes
tmux new-session -s anime \; \
  send-keys 'termisan -t naruto -c claude' Enter \; \
  split-window -h \; \
  send-keys 'termisan -t dragonball -c codex' Enter \; \
  split-window -v \; \
  send-keys 'termisan -t demonslayer -c claude -- --project ./api' Enter
```

```
┌─────────────────────────────┬─────────────────────────────┐
│ 🍥 Naruto Theme             │ 🐉 Dragon Ball Theme        │
│                             │                             │
│  $ claude                   ├─────────────────────────────┤
│  > Working on frontend...   │ ⚔️ Demon Slayer Theme       │
│                             │                             │
│                             │  $ claude --project ./api   │
│                             │  > Working on API...        │
└─────────────────────────────┴─────────────────────────────┘
```

#### Method 3: Ghostty Split Panes (Recommended)

Ghostty has **native split panes** — no tmux needed:

```
Cmd+D         → Split right  (macOS)
Cmd+Shift+D   → Split down   (macOS)
Ctrl+Shift+D  → Split right  (Linux)
```

Launch Termisan in each pane:

```
┌──────────────────────────────┬──────────────────────────────┐
│ ━━━━ 🍥 Naruto 🍥 ━━━━━━━━ │ ━━━━ 🐉 Dragon Ball 🐉 ━━━ │
│ Believe it! Let's code!      │ Power up your code!          │
│ ─── "I never go back on my  │ ─── "It's over 9000!" ───── │
│       word" ────────────     │                              │
│                              │  $ codex                     │
│  $ claude                    │  > Generating tests...       │
│  > Reviewing your PR...      │                              │
│                              │                              │
│ ⚡ Ninja Way │TERMISAN│14:30 │ ⚡ Saiyan Mode│TERMISAN│14:30│
└──────────────────────────────┴──────────────────────────────┘
```

### Multi-Agent Workflow Examples

#### Frontend + Backend Split

```bash
# Terminal/Pane 1: Frontend agent
termisan -t spyfamily -c claude -- --project ./frontend

# Terminal/Pane 2: Backend agent
termisan -t sololeveling -c claude -- --project ./backend
```

#### Code + Tests Split

```bash
# Pane 1: Writing code
termisan -t jjk -c claude

# Pane 2: Running tests and reviewing
termisan -t chainsawman -c codex -- --review
```

#### Multiple Claude Sessions with Different Models

```bash
# Pane 1: Fast iteration with Haiku
termisan -t pokemon -c claude -- --model haiku

# Pane 2: Deep analysis with Opus
termisan -t deathnote -c claude -- --model opus
```

---

## 7. Ghostty Terminal Integration

[Ghostty](https://ghostty.org/) is the recommended terminal for Termisan — it's fast, GPU-accelerated, and supports custom shaders for anime effects.

### Why Ghostty?

| Feature | Benefit for Termisan |
|---------|---------------------|
| **2ms latency** | Anime frame renders with zero lag |
| **Custom GLSL shaders** | Per-theme visual effects (glow, CRT, particles) |
| **Native split panes** | Multi-agent sessions without tmux |
| **Built-in Nerd Fonts** | All icons and sprites render perfectly |
| **300+ themes** | Base themes complement Termisan's ANSI overlay |
| **GPU-accelerated** | Shader effects don't slow down the terminal |
| **AppleScript API** | Automate themed window creation (macOS) |

### Installing Ghostty

```bash
# macOS — Download from https://ghostty.org/download
# Or with Homebrew:
brew install ghostty

# Linux (various)
# Arch:   pacman -S ghostty
# Fedora: dnf install ghostty
# Ubuntu: snap install ghostty  # or build from source
# NixOS:  nix-env -iA nixpkgs.ghostty
```

### Recommended Ghostty Config for Termisan

Create/edit `~/.config/ghostty/config`:

```
# Font — Nerd Font for full icon support
font-family = JetBrains Mono Nerd Font
font-size = 14

# Appearance
background-opacity = 0.95
background-blur-radius = 20
window-padding-x = 8
window-padding-y = 4

# Theme — a good dark base for Termisan's ANSI colors
theme = dark:Catppuccin Mocha,light:Catppuccin Latte

# Enable animated shaders (for future Termisan shader packs)
custom-shader-animation = true

# Shell integration for prompt navigation
shell-integration = detect

# Native tabs and splits
window-decoration = true
```

### Ghostty Keyboard Shortcuts

#### Window & Tab Management

| Action | macOS | Linux |
|--------|-------|-------|
| New window | `Cmd+N` | `Ctrl+Shift+N` |
| New tab | `Cmd+T` | `Ctrl+Shift+T` |
| Close tab/pane | `Cmd+W` | `Ctrl+Shift+W` |
| Next tab | `Cmd+Shift+]` | `Ctrl+PgDown` |
| Previous tab | `Cmd+Shift+[` | `Ctrl+PgUp` |
| Undo close | `Cmd+Z` | — |

#### Split Panes

| Action | macOS | Linux |
|--------|-------|-------|
| Split right | `Cmd+D` | `Ctrl+Shift+D` |
| Split down | `Cmd+Shift+D` | `Ctrl+Shift+Enter` |
| Navigate panes | `Cmd+[` / `Cmd+]` | `Ctrl+Shift+[` / `]` |
| Equalize panes | — | Drag dividers |

#### Navigation

| Action | macOS | Linux |
|--------|-------|-------|
| Command palette | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Jump to prompt | `Cmd+Up/Down` | `Ctrl+Shift+Up/Down` |
| Reload config | `Cmd+Shift+,` | `Ctrl+Shift+,` |
| Toggle inspector | `Cmd+Shift+I` | `Ctrl+Shift+I` |
| Quick terminal | `Global hotkey` | — |

### Ghostty CLI Tools

```bash
# Browse and preview themes
ghostty +list-themes

# List available fonts (verify Nerd Font is installed)
ghostty +list-fonts

# Show current keybindings
ghostty +list-keybinds

# Validate your config file
ghostty +validate-config

# Show resolved config
ghostty +show-config
```

### Setting Up Multi-Agent Sessions in Ghostty

#### Manual Setup

1. Open Ghostty
2. `Cmd+D` to split right → run `termisan -t naruto -c claude` in left pane
3. Click right pane → run `termisan -t dragonball -c codex`
4. `Cmd+Shift+D` in right pane to split down → run `termisan -t deathnote -c claude`

#### AppleScript Automation (macOS)

Create `~/scripts/termisan-multi.applescript`:

```applescript
tell application "Ghostty"
    activate

    -- Create first window with Naruto theme
    tell front window
        tell front tab
            tell front terminal
                write "termisan -t naruto -c claude -- --project ./frontend"
            end tell
        end tell

        -- Split right for backend agent
        set current tab to make new tab
        tell front tab
            tell front terminal
                write "termisan -t sololeveling -c claude -- --project ./backend"
            end tell
        end tell
    end tell
end tell
```

Run it:

```bash
osascript ~/scripts/termisan-multi.applescript
```

#### Shell Script Launcher

Create `~/scripts/termisan-multi.sh`:

```bash
#!/bin/bash
# Launch a multi-agent Termisan workspace in Ghostty

# Open first Ghostty window
ghostty -e termisan -t naruto -c claude &

# Give it a moment to start
sleep 1

# Open second window
ghostty -e termisan -t dragonball -c codex &

# Open third window
ghostty -e termisan -t demonslayer -c claude -- --project ./api &

echo "Launched 3 Termisan agents!"
```

```bash
chmod +x ~/scripts/termisan-multi.sh
./scripts/termisan-multi.sh
```

### Future: Ghostty Shader Packs

Termisan plans to ship **per-theme GLSL shaders** for Ghostty:

| Theme | Shader Effect |
|-------|--------------|
| Dragon Ball Z | Orange energy aura glow |
| Death Note | Dark vignette + red tint |
| Demon Slayer | Flame breathing glow on edges |
| Cyberpunk: Edgerunners | CRT scanlines + glitch effects |
| Solo Leveling | Purple shadow particle overlay |
| Attack on Titan | Film grain + desaturation |
| Pokémon | Bright bloom around text |
| Cowboy Bebop | Retro VHS static overlay |

---

## 8. Platform-Specific Notes

### macOS

- **Terminal**: Ghostty (recommended), iTerm2, Terminal.app, Kitty, Alacritty
- **PTY**: Native `pty.fork()` — full raw mode, perfect interactivity
- **Resize**: Handled via `SIGWINCH` signal
- **Install**: `pip install termisan` (no extra deps)
- **Best experience**: Ghostty with GPU shaders

### Linux

- **Terminal**: Ghostty (recommended), Kitty, Alacritty, GNOME Terminal, Konsole
- **PTY**: Native `pty.fork()` — identical to macOS behavior
- **Resize**: Handled via `SIGWINCH` signal
- **Install**: `pip install termisan` (no extra deps)
- **Note**: Ensure your terminal supports 24-bit color (`COLORTERM=truecolor`)

### Windows

- **Terminal**: [Windows Terminal](https://aka.ms/terminal) (recommended), ConEmu, PowerShell 7+
- **PTY**: Uses ConPTY via `pywinpty` (auto-installed)
- **Fallback**: Subprocess + threaded I/O if `pywinpty` is unavailable
- **ANSI**: Automatically enables Virtual Terminal Processing (Windows 10 1809+)
- **Install**: `pip install termisan` (installs `pywinpty` automatically)
- **Note**: Legacy `cmd.exe` has limited ANSI support — use Windows Terminal

#### Windows Terminal Recommended Settings

Open Windows Terminal settings (`Ctrl+,`) and set:

```json
{
    "profiles": {
        "defaults": {
            "font": {
                "face": "JetBrainsMono Nerd Font",
                "size": 14
            },
            "colorScheme": "One Half Dark",
            "useAcrylic": true,
            "acrylicOpacity": 0.95
        }
    }
}
```

---

## 9. Troubleshooting

### "Neither claude nor codex found in PATH"

Install one of the supported AI CLIs:

```bash
npm install -g @anthropic-ai/claude-code   # Claude
npm install -g @openai/codex               # Codex
```

### Colors look wrong / no colors

- Ensure your terminal supports 24-bit (truecolor):
  ```bash
  echo $COLORTERM  # Should show "truecolor" or "24bit"
  ```
- On older terminals, set `TERM=xterm-256color`
- On Windows, use **Windows Terminal** (not legacy cmd.exe)

### Header/footer not rendering

- Terminal must be at least **80 columns wide** and **10 rows tall**
- Check that your terminal supports VT100 scroll regions
- On Windows, ensure ANSI is enabled (Termisan does this automatically on Win 10+)

### Windows: "pywinpty not found" warning

```bash
pip install pywinpty
```

If pywinpty fails to install, Termisan falls back to subprocess mode (slightly less interactive but still functional).

### Terminal resize not working

- **macOS/Linux**: Should work automatically (SIGWINCH)
- **Windows**: Works best in Windows Terminal; resize may require restarting the session in legacy terminals

### Sprites/icons look broken

Install a [Nerd Font](https://www.nerdfonts.com/) for full icon support:

```bash
# macOS
brew install font-jetbrains-mono-nerd-font

# Linux
# Download from https://www.nerdfonts.com/font-downloads
# Extract to ~/.local/share/fonts/ and run fc-cache -fv
```

Set your terminal to use the Nerd Font variant.

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────────┐
│                    TERMISAN QUICK REFERENCE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  LAUNCH          termisan                                       │
│  WITH THEME      termisan -t naruto                             │
│  WITH COMMAND    termisan -c claude                             │
│  WITH ARGS       termisan -t dragonball -c claude -- --model op │
│  LIST THEMES     termisan -l                                    │
│  PREVIEW THEME   termisan -p deathnote                          │
│  VERSION         termisan -v                                    │
│                                                                 │
│  MULTI-AGENT (tmux)                                             │
│    tmux new \; send-keys 'termisan -t naruto' Enter \;          │
│    split-window -h \; send-keys 'termisan -t dragonball' Enter  │
│                                                                 │
│  MULTI-AGENT (Ghostty)                                          │
│    Cmd+D split right → run termisan in each pane                │
│                                                                 │
│  PLATFORMS       macOS ✓   Linux ✓   Windows ✓                  │
│  THEMES          20 (10 classic + 10 modern)                    │
│  TERMINALS       Ghostty, iTerm2, Kitty, Windows Terminal, etc. │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```
