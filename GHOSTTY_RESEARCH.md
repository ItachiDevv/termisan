# Ghostty Terminal Research for Termisan

> Research compiled March 2026 — evaluating Ghostty as a target terminal for the Termisan anime-themed terminal wrapper.

---

## 1. What is Ghostty?

Ghostty is a **fast, feature-rich, cross-platform terminal emulator** that uses **platform-native UI** and **GPU acceleration**. It was created by **Mitchell Hashimoto** (founder of HashiCorp/Terraform/Vagrant) as a side project starting in 2023, open-sourced in late 2024, and has rapidly become one of the most popular modern terminal emulators.

- **Written in**: Zig (core) + Swift/AppKit (macOS) + GTK4 (Linux)
- **License**: MIT
- **Non-profit stewardship**: Moved under Hack Club's 501(c)(3) umbrella in 2025
- **Latest release**: v1.3.0 (March 2026) — 2,800+ commits from 180 contributors
- **GitHub**: [ghostty-org/ghostty](https://github.com/ghostty-org/ghostty)

---

## 2. Platform Support (NOT Mac-Only!)

**Important correction**: Ghostty is **NOT** macOS-only. It supports:

| Platform | Status | UI Toolkit | GPU Backend |
|----------|--------|------------|-------------|
| **macOS** | Full support (binary available) | Swift + AppKit + SwiftUI | **Metal** |
| **Linux** | Full support (packages + source) | **GTK4** | **OpenGL** |
| **Windows** | Not yet supported | Planned | TBD |

On macOS it feels like a native Apple app (real AppKit windows, native tabs, native splits). On Linux it uses GTK4 with full Wayland and X11 support.

---

## 3. Performance — Best-in-Class

### Raw Speed Benchmarks
| Terminal | 100K lines cat | Input Latency |
|----------|----------------|---------------|
| **Ghostty** | **0.7s** | **2ms** |
| Alacritty | ~0.8s | 3ms |
| Kitty | ~1.2s | 3ms |
| iTerm2 | ~2.8s | 12ms |

- **4x faster** than iTerm2 and Kitty for plain text rendering
- **2x faster** than Terminal.app
- Comparable to Alacritty (sometimes faster)
- **48% less memory** than iTerm2 in multi-tab scenarios
- 2ms key-to-screen latency — at the threshold of human perception

### Why It's Fast
- Custom GPU renderer written in Zig
- Metal on macOS (only terminal besides iTerm2 to use Metal directly)
- OpenGL on Linux
- The **only** Metal-based terminal that supports ligatures without CPU fallback
- Minimal abstraction layers between input and pixels

---

## 4. UI/UX Design — Native & Beautiful

### Native Platform Integration
- **macOS**: Real AppKit windows, native tabs, native split panes, proper menu bar, settings GUI
- **Linux**: GTK4 with libadwaita for a native GNOME feel
- Everything feels like a first-party OS app, not an Electron wrapper

### Window Management
- Multiple windows, each with its own tabs and splits
- Native tab bar (not custom-drawn)
- Native split panes with drag-to-resize
- **Quick Terminal**: Animates down from the menu bar for instant access (like Quake-style dropdown)

### Typography
- Ships with **JetBrains Mono** as default font
- Full **ligature support** (GPU-accelerated!)
- Built-in **Nerd Fonts** — icons work out of the box
- Excellent Unicode and emoji rendering

### macOS-Specific UI Niceties
- **Proxy Icon**: Drag the title bar icon to access/move terminal session files
- **Quick Look**: Three-finger tap or force touch for definitions/web search
- **Secure Keyboard Entry**: Animated lock icon when entering passwords
- **Native scrollbars** (new in 1.3)
- **Touch Bar support**

---

## 5. Theming — Hundreds Built-In

### Built-In Themes
- Ships with **hundreds of themes** sourced from iterm2-color-schemes
- Updated weekly on the main branch
- Browse with `ghostty +list-themes` CLI command
- Popular choices: Catppuccin, Nord, Monokai, Dracula, Tokyo Night, Gruvbox, etc.

### Automatic Light/Dark Switching
```
theme = light:Catppuccin Latte,dark:Catppuccin Mocha
```
Ghostty auto-switches themes when the OS switches between light and dark mode.

### Custom Themes
- Full control over all 16 ANSI colors + foreground/background/cursor/selection
- Transparency and blur support (glassmorphic appearance)

---

## 6. Custom Shaders — The Fun Factor

This is where Ghostty gets **really fun** for a terminal wrapper project:

### What Are Ghostty Shaders?
Ghostty supports **custom GLSL shaders** that post-process the terminal output on the GPU. This is extremely rare among terminals.

### Configuration
```
custom-shader = ~/.config/ghostty/shaders/crt.glsl
custom-shader-animation = true
```

### Popular Shader Effects
- **CRT scanlines** with chromatic aberration and phosphor glow
- **Bloom/glow** effects around text
- **Retro dot-matrix** look
- **Cursor blaze/trail** — cursor leaves a visual trail as it moves (new in 1.2)
- **Matrix rain** overlays
- **VHS static** effects
- Shaders can be **stacked** (applied in order)

### Community Resources
- [Awesome Ghostty](https://github.com/fearlessgeekmedia/awesome-ghostty) — curated list of shaders and tools
- [Fun with Ghostty Shaders](https://catskull.net/fun-with-ghostty-shaders.html) — guide to stacking shaders

### Relevance to Termisan
**This is huge for an anime-themed wrapper.** Imagine:
- Anime-specific shader effects per theme (glow for Dragon Ball Z, dark vignette for Death Note)
- Cursor trail effects matching the character's powers
- Background animation shaders
- Theme-specific post-processing

---

## 7. Configuration — Dead Simple

### Format
Plain text key-value pairs at `~/.config/ghostty/config`:
```
font-family = JetBrains Mono
font-size = 14
theme = Catppuccin Mocha
background-opacity = 0.9
custom-shader = ~/.config/ghostty/shaders/bloom.glsl
window-padding-x = 10
window-padding-y = 10
```

### Key Properties
- **Zero config needed** — works beautifully out of the box
- **Live reload** — `Cmd+Shift+,` (macOS) or `Ctrl+Shift+,` (Linux) reloads config instantly
- **Cross-platform configs** — same config file works on macOS and Linux
- **Optional includes**: `config-file = ?~/.config/ghostty/local-config` (prefixed with `?` for optional)
- **Hundreds of options** available

### Notable Config Options for Termisan
| Option | What it does |
|--------|-------------|
| `theme` | Set color theme (with light/dark auto-switch) |
| `background-opacity` | Window transparency (0.0 - 1.0) |
| `background-blur-radius` | Blur behind transparent terminal |
| `custom-shader` | Apply GLSL shader effects |
| `custom-shader-animation` | Enable animated shaders |
| `font-family` | Set font (nerd fonts built-in) |
| `window-padding-x/y` | Inner padding |
| `window-decoration` | Show/hide window chrome |
| `cursor-style` | block, bar, underline |
| `cursor-color` | Cursor color |
| `title` | Custom window title |
| `window-title-font-family` | Custom title bar font |
| `resize-overlay` | Show size overlay on resize |

---

## 8. Terminal Protocol Support

Ghostty has best-in-class protocol support:

| Protocol | Supported | Notes |
|----------|-----------|-------|
| **Kitty Graphics Protocol** | Yes | Render images inline in terminal |
| **Kitty Keyboard Protocol** | Yes | Enhanced keyboard input handling |
| **Sixel Graphics** | Yes | Legacy image protocol |
| **Synchronized Rendering** | Yes | Flicker-free updates |
| **OSC Color Queries** | Yes | Apps can query/set colors |
| **Light/Dark Mode Notifications** | Yes | Apps notified of OS theme changes |
| **Shell Integration** | Yes | bash, zsh, fish, elvish (auto-injected) |

### Shell Integration Features
- Triple-click + Cmd to select entire command output
- `jump_to_prompt` keybinding to navigate between prompts
- Alt+click to move cursor to click position
- Command completion notifications (1.3)

---

## 9. Keybindings — Powerful & Modal

### Custom Keybinds
```
keybind = cmd+shift+t=new_tab
keybind = cmd+d=new_split:right
```

### Advanced Prefixes
- `global:` — Works even when Ghostty isn't focused (macOS, needs accessibility permissions)
- `all:` — Applies to all terminal surfaces
- `unconsumed:` — Passes input to the running program if not handled
- `performable:` — Only consumes input if the action can be performed

### Modal Keybindings (1.3)
New in 1.3 — **key tables** for modal keybinding workflows similar to tmux:
- Chain keybindings (e.g., press a leader key, then a second key)
- `catch_all` key option
- Enables tmux-like workflows without tmux

---

## 10. AppleScript API (macOS) — Automation

New in 1.3 (preview), Ghostty exposes a **native AppleScript dictionary**:

```applescript
tell application "Ghostty"
    tell front window
        set current tab to make new tab
        tell front tab
            tell front terminal
                write "echo hello"
            end tell
        end tell
    end tell
end tell
```

### Capabilities
- Create/query/control windows, tabs, splits
- Send text, key, and mouse input
- Perform any keybind action programmatically
- Inspect terminal state
- Integration with Alfred, Raycast, and other macOS automation tools

### Relevance to Termisan
AppleScript means Termisan could:
- Programmatically create themed Ghostty windows
- Set up multi-pane layouts with different anime themes
- Send commands to specific terminals
- Build a macOS-native launcher for themed sessions

---

## 11. Terminal Inspector — Developer Tool

Ghostty includes a **built-in terminal inspector** — a real-time debugging tool that shows:
- Keystroke processing
- Escape sequence parsing
- Render timings
- Internal terminal state

This is invaluable for terminal application developers and would help with Termisan development/debugging.

---

## 12. Command Completion Notifications (1.3)

Ghostty can alert users when long-running commands finish:
- Desktop notifications
- Terminal bells
- Configurable to only trigger for unfocused windows
- Great for long builds or AI CLI sessions

---

## 13. Rich Copy (1.3)

New clipboard handling places **multiple formats** (plain text + HTML) on the clipboard:
- Paste into rich text editors with **color and styling preserved**
- Copy terminal output as formatted text

---

## 14. How Ghostty Compares

| Feature | Ghostty | iTerm2 | Alacritty | Kitty | Warp |
|---------|---------|--------|-----------|-------|------|
| **Speed** | Fastest | Slowest | Very fast | Fast | Medium |
| **Latency** | 2ms | 12ms | 3ms | 3ms | 8ms |
| **GPU** | Metal/OpenGL | Metal | OpenGL | OpenGL | Metal |
| **Native UI** | Yes | Yes | No | No | Yes |
| **Ligatures** | Yes (GPU) | Yes | No | Yes | Yes |
| **Custom Shaders** | Yes | No | No | No | No |
| **Image Protocol** | Kitty+Sixel | iTerm | No | Kitty | No |
| **Config Format** | Key-value | GUI | TOML | Conf | GUI |
| **Zero Config** | Yes | Yes | No | No | Yes |
| **Nerd Fonts Built-in** | Yes | No | No | No | Yes |
| **AppleScript** | Yes (1.3) | Yes | No | No | No |
| **Linux Support** | Yes (GTK4) | No | Yes | Yes | No |
| **Free** | Yes | Yes | Yes | Yes | Freemium |
| **Open Source** | Yes (MIT) | Yes (GPL) | Yes | Yes | Partially |

---

## 15. Limitations & Downsides

- **No Windows support** (yet)
- **No tmux integration** — some users report sluggishness with tmux (compared to Alacritty)
- **Relatively new** — some edge cases and bugs still being ironed out
- **AppleScript API** is still in preview (may change in 1.4)
- **GPU requirement** — needs OpenGL 4.1+ on Linux, which can be an issue on minimal/server setups
- **No plugin system** — extensibility is through config, shaders, and AppleScript only
- **Zig build dependency** — building from source requires Zig, which some distros don't package

---

## 16. Relevance to Termisan — Opportunities

### Why Ghostty is Perfect for an Anime Terminal Wrapper

1. **Custom Shaders** — The killer feature. Termisan could ship anime-themed GLSL shaders:
   - Energy aura effects for Dragon Ball Z
   - Dark vignette + red tint for Death Note
   - Cherry blossom particle effects for Demon Slayer
   - Cyberpunk scan lines for Cyberpunk: Edgerunners
   - Glitch effects for Solo Leveling shadow summons

2. **Programmatic Themes** — Termisan could generate Ghostty theme configs from its existing theme definitions (hex colors map directly to Ghostty's color config)

3. **AppleScript Automation** — On macOS, Termisan could:
   - Launch themed Ghostty windows with the right config
   - Set up multi-pane anime dashboards
   - Switch themes dynamically

4. **Config Generation** — Termisan's Python themes could generate complete Ghostty config files:
   ```python
   # Convert Termisan theme to Ghostty config
   def theme_to_ghostty(theme):
       return f"""
   theme = custom
   background = {theme['primary']}
   foreground = {theme['accent']}
   cursor-color = {theme['secondary']}
   custom-shader = ~/.config/ghostty/shaders/{theme['name']}.glsl
   custom-shader-animation = true
   font-family = JetBrains Mono Nerd Font
   background-opacity = 0.95
   background-blur-radius = 20
   """
   ```

5. **Native Feel** — Unlike wrapping with PTY + ANSI (current approach), a Ghostty integration would feel like a native app while still being themed

6. **Performance** — Ghostty's 2ms latency and GPU rendering mean anime-themed shaders won't slow down the terminal

7. **Zero Config Base** — Users don't need to configure anything before Termisan customizes their Ghostty

### Potential Architecture

```
Termisan CLI
├── Current: PTY wrapper with ANSI art (works in any terminal)
└── New: Ghostty integration mode
    ├── Generate Ghostty config from anime theme
    ├── Generate/install GLSL shaders per theme
    ├── Launch Ghostty with custom config
    ├── AppleScript automation (macOS)
    └── D-Bus automation (Linux)
```

---

## 17. Additional Deep-Dive Notes

### Origin Story
Mitchell Hashimoto started Ghostty in **2022** as a hobby project to learn **Zig** and explore graphics programming. He had no plan to release it publicly but discovered existing terminals forced unacceptable tradeoffs. He opened a Discord server in 2023 — **28,000 people** joined, ~5,000 were selected for private beta. After nearly 2 years of beta testing, **Ghostty 1.0 launched December 26, 2024** under MIT license. The GitHub repo now has **~46,000+ stars**, making it the most-starred terminal emulator on GitHub.

### Architecture — libghostty
The core is a **cross-platform C-ABI compatible library called `libghostty`**, with platform-specific GUI layers on top. The heavy lifting (terminal emulation, font handling, rendering) lives in the shared Zig core, while each platform gets a truly native GUI shell. A sub-library `libghostty-vt` (terminal sequence parsing) targets Zig, C, and even **WebAssembly**.

### Sixel — Explicitly NOT Supported
Ghostty **will not** add Sixel support. The maintainer considers Sixel to have too many unspecified edge cases and poor library quality. They back the Kitty graphics protocol as the superior alternative. This matters because tmux/Zellij only support Sixel (not Kitty graphics), so inline images don't work inside multiplexers.

### Quick Terminal (Quake Mode)
Global hotkey summons a slide-down terminal from the screen edge. State persists between toggles. Configurable animation duration. Currently **macOS only**.

### Command Palette
Searchable palette (`Cmd+Shift+P`) exposing all actions — similar to VS Code. Future plans include letting running programs (e.g., Neovim) expose their own commands in the palette.

### CLI Tools
```bash
ghostty +list-themes     # Browse available themes
ghostty +list-fonts      # List available fonts
ghostty +list-keybinds   # Show all keybindings
ghostty +show-config     # Show current config
ghostty +validate-config # Validate config file
```

### Community Sites
- [ghostty.style](https://github.com/ghostty-org/ghostty/discussions/10928) — 460+ community themes
- [ghostty.town](https://ghostty.town) — User-submitted configurations
- [ghostty-config](https://github.com/zerebos/ghostty-config) — Web-based config generator
- [ghostty-shaders](https://github.com/0xhckr/ghostty-shaders) — Community shader effects

### App Intents (macOS)
Ghostty can be automated via **Apple Shortcuts** using App Intents, in addition to AppleScript.

### Accessibility API (macOS)
Read-only accessibility for screen readers and AI tools (opt-in, requires permissions). This could be useful for Termisan to read terminal state.

### Undo Close
You can **undo closing a tab or window** — a small but delightful feature.

---

## Sources

- [Ghostty Official Website](https://ghostty.org/)
- [Ghostty GitHub Repository](https://github.com/ghostty-org/ghostty)
- [Ghostty Features Documentation](https://ghostty.org/docs/features)
- [Ghostty Configuration Reference](https://ghostty.org/docs/config/reference)
- [Ghostty 1.3.0 Release Notes](https://ghostty.org/docs/install/release-notes/1-3-0)
- [Ghostty AppleScript Docs](https://ghostty.org/docs/features/applescript)
- [Ghostty Keybindings Docs](https://ghostty.org/docs/config/keybind)
- [Ghostty Theme Docs](https://ghostty.org/docs/features/theme)
- [Fun with Ghostty Shaders](https://catskull.net/fun-with-ghostty-shaders.html)
- [Awesome Ghostty](https://github.com/fearlessgeekmedia/awesome-ghostty)
- [Best Terminal Emulators 2026 Comparison](https://www.devtoolreviews.com/reviews/best-terminal-emulators-2026)
- [Ghostty vs iTerm2](https://medium.com/@artemkhrenov/modern-terminal-emulators-ghostty-vs-iterm2-3cd5e55a8d24)
- [Modern Terminals Showdown](https://blog.codeminer42.com/modern-terminals-alacritty-kitty-and-ghostty/)
- [Ghostty 1.3 Release Coverage](https://linuxiac.com/ghostty-1-3-terminal-emulator-released-with-native-scrollbars/)
- [Ghostty Review 2026](https://dockshare.io/apps/ghostty)
- [14 Themes for Ghostty](https://itsfoss.com/ghostty-themes/)
- [Ghostty Terminal Features Review](https://itsfoss.com/ghostty-terminal-features/)
- [Choosing a Terminal on macOS 2025](https://medium.com/@dynamicy/choosing-a-terminal-on-macos-2025-iterm2-vs-ghostty-vs-wezterm-vs-kitty-vs-alacritty-d6a5e42fd8b3)
- [Ghostty 1.0 is Coming — Mitchell Hashimoto](https://mitchellh.com/writing/ghostty-is-coming)
- [Ghostty 1.0 has been summoned — LWN.net](https://lwn.net/Articles/1004377/)
- [Ghostty: A Modern Terminal for Developers — OpenReplay](https://blog.openreplay.com/ghostty-modern-terminal-developers/)
- [Ghostty Shaders Repository](https://github.com/0xhckr/ghostty-shaders)
- [ghostty.style Theme Gallery](https://github.com/ghostty-org/ghostty/discussions/10928)
- [Ghostty Config Generator](https://github.com/zerebos/ghostty-config)
- [Sixel Support Discussion](https://github.com/ghostty-org/ghostty/discussions/2496)
- [Ghostty Non-Profit Announcement](https://www.omgubuntu.co.uk/2025/12/ghostty-terminal-non-profit-fiscal-sponsorship)
