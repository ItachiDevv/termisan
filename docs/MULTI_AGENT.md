# Multi-Agent Sessions with Termisan

> Run multiple AI agents simultaneously, each in their own anime-themed terminal.

---

## Overview

Termisan supports running multiple independent sessions. Each session wraps a
separate AI CLI process (Claude, Codex, or any command) with its own theme.
This lets you run parallel agents for different parts of your project.

---

## Architectures

### 1. Separate Windows

The simplest approach — one Termisan per terminal window.

```
┌─ Window 1 ────────────────────┐  ┌─ Window 2 ────────────────────┐
│ ━━ 🍥 Naruto 🍥 ━━━━━━━━━━━━ │  │ ━━ 🐉 Dragon Ball Z 🐉 ━━━━ │
│ Believe it! Let's code!       │  │ Power up your code!           │
│ ─── "I never go back on my   │  │ ─── "It's over 9000!" ─────  │
│       word!" ────────────     │  │                               │
│                               │  │                               │
│  claude> Working on the       │  │  codex> Generating unit       │
│  frontend components...       │  │  tests for the API...         │
│                               │  │                               │
│ ⚡ Ninja Way │TERMISAN│14:30  │  │ ⚡ Saiyan │TERMISAN│14:30     │
└───────────────────────────────┘  └───────────────────────────────┘
```

```bash
# In terminal window 1
termisan -t naruto -c claude -- --project ./frontend

# In terminal window 2
termisan -t dragonball -c codex -- --project ./backend
```

### 2. tmux Multiplexer

Run everything in one terminal window with tmux panes.

```
┌─────────────────────────────────────────────────────────────────┐
│ tmux session: anime-dev                                         │
├────────────────────────────────┬────────────────────────────────┤
│ ━━ 🍥 Naruto ━━━━━━━━━━━━━━  │ ━━ ☠️ One Piece ━━━━━━━━━━━━  │
│ Believe it!                   │ Set sail for the code!         │
│ ─── "That's my ninja way" ── │ ─── "I'm gonna be King" ───── │
│                               │                                │
│  claude> Refactoring the     │  claude> Reviewing PR #42      │
│  auth middleware...           │  for security issues...        │
│                               │                                │
│ ⚡ Ninja │TERMISAN│14:30      │ ⚡ Pirate │TERMISAN│14:30      │
├────────────────────────────────┴────────────────────────────────┤
│ ━━ 💀 Death Note ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│ Write the code's name in the notebook...                        │
│ ─── "I am justice!" ───────────────────────────────────────     │
│                                                                 │
│  claude> Analyzing performance bottlenecks in database layer... │
│                                                                 │
│ ⚡ Kira Mode │TERMISAN│14:30│ L Investigation                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Setup Script

```bash
#!/bin/bash
# termisan-workspace.sh — Launch a multi-agent tmux workspace

SESSION="anime-dev"

# Create session with first pane
tmux new-session -d -s "$SESSION" -x 200 -y 50

# Pane 1: Frontend agent (Naruto theme)
tmux send-keys -t "$SESSION" \
  'termisan -t naruto -c claude -- --project ./frontend' Enter

# Pane 2: Backend agent (One Piece theme) — split right
tmux split-window -h -t "$SESSION"
tmux send-keys -t "$SESSION" \
  'termisan -t onepiece -c claude -- --project ./backend' Enter

# Pane 3: Database/perf agent (Death Note theme) — split below
tmux split-window -v -t "$SESSION"
tmux send-keys -t "$SESSION" \
  'termisan -t deathnote -c claude -- --project ./database' Enter

# Equalize panes
tmux select-layout -t "$SESSION" tiled

# Attach
tmux attach -t "$SESSION"
```

#### tmux Navigation

| Action | Keys |
|--------|------|
| Switch pane | `Ctrl+B` then arrow key |
| Resize pane | `Ctrl+B` then `Ctrl+arrow` |
| Zoom pane (fullscreen toggle) | `Ctrl+B` then `Z` |
| New pane (horizontal split) | `Ctrl+B` then `"` |
| New pane (vertical split) | `Ctrl+B` then `%` |
| Kill pane | `Ctrl+B` then `X` |
| Detach (leave running) | `Ctrl+B` then `D` |
| Reattach | `tmux attach -t anime-dev` |

### 3. Ghostty Native Splits (Recommended)

Ghostty has built-in split panes — no tmux needed. Faster and more native feeling.

```
┌──────────────────────────────────────────────────────────────────┐
│ Ghostty                                                          │
├─────────────────────────────────┬────────────────────────────────┤
│ ━━ 🍥 Naruto 🍥 ━━━━━━━━━━━━ │ ━━ ⚔️ Demon Slayer ⚔️ ━━━━━━ │
│ Believe it! Let's code!        │ Breathe and focus...           │
│ ─── "I never go back..." ──── │ ─── "Go beyond your..." ───── │
│                                │                                │
│  claude> Building React       │  claude> Writing E2E tests     │
│  components for the           │  for the checkout flow...      │
│  dashboard...                 │                                │
│                                │                                │
│ ⚡ Ninja Way │TERMISAN│14:30   │ ⚡ Water Breathing │14:30      │
└─────────────────────────────────┴────────────────────────────────┘
```

#### Ghostty Split Shortcuts

| Action | macOS | Linux |
|--------|-------|-------|
| Split right | `Cmd+D` | `Ctrl+Shift+D` |
| Split down | `Cmd+Shift+D` | `Ctrl+Shift+Enter` |
| Navigate splits | `Cmd+[` / `Cmd+]` | `Ctrl+Shift+[` / `]` |
| Close split | `Cmd+W` | `Ctrl+Shift+W` |
| New tab | `Cmd+T` | `Ctrl+Shift+T` |
| New window | `Cmd+N` | `Ctrl+Shift+N` |

#### Step-by-Step

1. Open Ghostty
2. Run `termisan -t naruto -c claude -- --project ./frontend`
3. Press `Cmd+D` (macOS) or `Ctrl+Shift+D` (Linux) to split right
4. In the new pane: `termisan -t demonslayer -c claude -- --project ./backend`
5. Press `Cmd+Shift+D` (macOS) to split down in the right pane
6. In the new pane: `termisan -t sololeveling -c claude -- --project ./tests`

---

## Workflow Patterns

### Pattern 1: Feature Development (2 Agents)

```bash
# Agent 1: Writes the feature code
termisan -t jjk -c claude -- --project ./src

# Agent 2: Writes tests for the feature
termisan -t chainsawman -c codex -- --project ./tests
```

### Pattern 2: Full-Stack (3 Agents)

```bash
# Frontend
termisan -t spyfamily -c claude -- --project ./frontend

# Backend API
termisan -t sololeveling -c claude -- --project ./api

# Infrastructure / DevOps
termisan -t cyberpunk -c claude -- --project ./infra
```

### Pattern 3: Code Review Pipeline (2 Agents)

```bash
# Agent 1: Makes changes
termisan -t naruto -c claude

# Agent 2: Reviews the changes (separate project checkout)
termisan -t deathnote -c claude -- --project ./review-copy
```

### Pattern 4: Fast vs Deep (2 Agents, Different Models)

```bash
# Fast agent — quick iterations with Haiku
termisan -t pokemon -c claude -- --model haiku

# Deep agent — thorough analysis with Opus
termisan -t aot -c claude -- --model opus
```

### Pattern 5: Cross-Language (2+ Agents)

```bash
# Python backend
termisan -t frieren -c claude -- --project ./python-api

# TypeScript frontend
termisan -t oshinoko -c claude -- --project ./react-app

# Rust microservice
termisan -t bleach -c claude -- --project ./rust-service
```

---

## Tips

1. **Use different themes per agent** — makes it easy to visually distinguish which agent is doing what at a glance.

2. **Match theme to purpose** — Use serious themes (Death Note, Attack on Titan) for critical tasks like security reviews, fun themes (Pokémon, Spy x Family) for exploratory work.

3. **Use `--project` flags** — keep agents scoped to specific directories so they don't step on each other's files.

4. **tmux sessions persist** — use `tmux detach` (`Ctrl+B D`) to leave agents running in the background, then reattach later with `tmux attach -t anime-dev`.

5. **Ghostty tabs for task groups** — put related agents in splits within the same tab, unrelated work in separate tabs.

6. **Monitor resource usage** — each agent consumes API tokens independently. Running 3+ agents simultaneously can burn through tokens quickly.
