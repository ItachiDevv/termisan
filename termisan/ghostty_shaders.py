"""Per-theme GLSL shader packs for Ghostty.

Each shader is a GLSL fragment shader that post-processes the terminal
output. Ghostty passes the rendered terminal as a texture and applies
the shader as a fullscreen quad.

Ghostty shader uniforms:
  - iTime: float (seconds since start)
  - iResolution: vec3 (viewport width, height, 1.0)
  - iChannelResolution: vec2[] (texture dimensions)
  - iChannel0: sampler2D (the terminal texture)
"""

import os
import sys
from pathlib import Path

from termisan.themes import ALL_THEMES, AnimeTheme


def _hex_to_vec3(hex_color: str) -> str:
    """Convert '#RRGGBB' to GLSL vec3(r, g, b) with 0.0-1.0 values."""
    h = hex_color.lstrip("#")
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return f"vec3({r:.3f}, {g:.3f}, {b:.3f})"


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SHADER TEMPLATES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def _shader_energy_aura(theme: AnimeTheme) -> str:
    """Pulsing energy aura glow on screen edges. Used by: Dragon Ball Z."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Energy Aura
// Pulsing glow on screen edges

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Distance from edge
    float edgeDist = min(min(uv.x, 1.0 - uv.x), min(uv.y, 1.0 - uv.y));

    // Pulsing intensity
    float pulse = 0.5 + 0.5 * sin(iTime * 2.0);
    float auraWidth = 0.08 + 0.03 * pulse;

    // Aura glow
    float aura = smoothstep(auraWidth, 0.0, edgeDist);
    vec3 auraColor = {color};
    float auraIntensity = aura * (0.3 + 0.2 * pulse);

    fragColor = vec4(tex.rgb + auraColor * auraIntensity, tex.a);
}}
"""


def _shader_dark_vignette(theme: AnimeTheme) -> str:
    """Dark vignette with tinted edges. Used by: Death Note, Attack on Titan."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Dark Vignette
// Heavy vignette with color-tinted darkness

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Vignette
    vec2 center = uv - 0.5;
    float dist = length(center);
    float vignette = 1.0 - smoothstep(0.3, 0.85, dist);

    // Subtle color tint in dark areas
    vec3 tint = {color};
    float tintAmount = (1.0 - vignette) * 0.15;

    vec3 result = tex.rgb * vignette + tint * tintAmount;
    fragColor = vec4(result, tex.a);
}}
"""


def _shader_flame_breathing(theme: AnimeTheme) -> str:
    """Animated flame-like glow on edges. Used by: Demon Slayer."""
    color = _hex_to_vec3(theme.color_primary)
    accent = _hex_to_vec3(theme.color_accent)
    return f"""\
// Termisan Shader: {theme.name} — Flame Breathing
// Animated fire glow along screen edges

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Distance from bottom and sides
    float bottomDist = uv.y;
    float sideDist = min(uv.x, 1.0 - uv.x);

    // Flame noise using sine waves
    float noise = sin(uv.x * 20.0 + iTime * 3.0) * 0.5 + 0.5;
    noise *= sin(uv.x * 13.0 - iTime * 2.0) * 0.5 + 0.5;

    // Bottom flame
    float flameHeight = 0.06 + 0.03 * noise;
    float flame = smoothstep(flameHeight, 0.0, bottomDist);

    // Side glow
    float sideGlow = smoothstep(0.05, 0.0, sideDist) * 0.3;

    vec3 flameColor = mix({color}, {accent}, noise);
    float intensity = flame * 0.5 + sideGlow;

    fragColor = vec4(tex.rgb + flameColor * intensity, tex.a);
}}
"""


def _shader_crt_glitch(theme: AnimeTheme) -> str:
    """CRT scanlines with glitch effects. Used by: Cyberpunk: Edgerunners."""
    color = _hex_to_vec3(theme.color_primary)
    accent = _hex_to_vec3(theme.color_secondary)
    return f"""\
// Termisan Shader: {theme.name} — CRT Glitch
// Scanlines + chromatic aberration + occasional glitch

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;

    // Chromatic aberration
    float aberration = 0.002;
    float r = texture(iChannel0, uv + vec2(aberration, 0.0)).r;
    float g = texture(iChannel0, uv).g;
    float b = texture(iChannel0, uv - vec2(aberration, 0.0)).b;
    vec3 color = vec3(r, g, b);

    // Scanlines
    float scanline = sin(fragCoord.y * 3.14159) * 0.04;
    color -= scanline;

    // Subtle glitch — horizontal shift on random lines
    float glitchTime = floor(iTime * 4.0);
    float glitchLine = fract(sin(glitchTime * 43.7) * 4378.5);
    float lineY = fract(fragCoord.y / iResolution.y);
    if (abs(lineY - glitchLine) < 0.005) {{
        float shift = sin(glitchTime * 13.0) * 0.02;
        color = texture(iChannel0, uv + vec2(shift, 0.0)).rgb;
    }}

    // Subtle color tint
    vec3 tint = {color};
    color = mix(color, color * (vec3(1.0) + tint * 0.1), 0.5);

    fragColor = vec4(color, 1.0);
}}
"""


def _shader_shadow_particles(theme: AnimeTheme) -> str:
    """Dark particle overlay. Used by: Solo Leveling."""
    color = _hex_to_vec3(theme.color_primary)
    accent = _hex_to_vec3(theme.color_secondary)
    return f"""\
// Termisan Shader: {theme.name} — Shadow Particles
// Rising dark particles with purple glow

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Generate particles
    float particles = 0.0;
    for (int i = 0; i < 8; i++) {{
        float fi = float(i);
        vec2 particlePos = vec2(
            fract(sin(fi * 127.1) * 43758.5),
            fract(fract(sin(fi * 311.7) * 43758.5) + iTime * (0.03 + 0.02 * fract(sin(fi * 78.3))))
        );
        float dist = length(uv - particlePos);
        particles += smoothstep(0.02, 0.0, dist) * 0.3;
    }}

    // Bottom shadow mist
    float mist = smoothstep(0.15, 0.0, uv.y) * 0.2;

    vec3 shadowColor = mix({color}, {accent}, 0.5);
    vec3 result = tex.rgb + shadowColor * (particles + mist);

    fragColor = vec4(result, tex.a);
}}
"""


def _shader_bloom(theme: AnimeTheme) -> str:
    """Bright bloom/glow around text. Used by: Pokemon, My Hero Academia."""
    return f"""\
// Termisan Shader: {theme.name} — Bloom
// Soft glow around bright text

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec2 texel = 1.0 / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Simple box blur for bloom
    vec3 bloom = vec3(0.0);
    for (int x = -2; x <= 2; x++) {{
        for (int y = -2; y <= 2; y++) {{
            vec2 offset = vec2(float(x), float(y)) * texel * 2.0;
            bloom += texture(iChannel0, uv + offset).rgb;
        }}
    }}
    bloom /= 25.0;

    // Only bloom bright areas
    float brightness = dot(bloom, vec3(0.299, 0.587, 0.114));
    float bloomMask = smoothstep(0.3, 0.8, brightness);

    vec3 result = tex.rgb + bloom * bloomMask * 0.3;
    fragColor = vec4(result, tex.a);
}}
"""


def _shader_film_grain(theme: AnimeTheme) -> str:
    """Film grain + slight desaturation. Used by: Attack on Titan, Cowboy Bebop."""
    return f"""\
// Termisan Shader: {theme.name} — Film Grain
// Subtle grain with slight desaturation for a cinematic feel

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Film grain
    float grain = fract(sin(dot(fragCoord.xy + iTime, vec2(12.9898, 78.233))) * 43758.5453);
    grain = (grain - 0.5) * 0.06;

    // Slight desaturation
    float luma = dot(tex.rgb, vec3(0.299, 0.587, 0.114));
    vec3 desaturated = mix(tex.rgb, vec3(luma), 0.15);

    vec3 result = desaturated + grain;
    fragColor = vec4(result, tex.a);
}}
"""


def _shader_vhs_static(theme: AnimeTheme) -> str:
    """VHS static overlay. Used by: Cowboy Bebop."""
    return f"""\
// Termisan Shader: {theme.name} — VHS Static
// Retro VHS tracking lines and noise

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Horizontal tracking lines
    float trackingSpeed = iTime * 0.5;
    float tracking = smoothstep(0.0, 0.01,
        abs(fract(uv.y * 3.0 + trackingSpeed) - 0.5) - 0.48);
    tracking *= 0.03;

    // Static noise
    float noise = fract(sin(dot(fragCoord.xy + fract(iTime), vec2(12.9898, 78.233))) * 43758.5);
    noise = (noise - 0.5) * 0.03;

    // Color bleed
    float bleed = 0.001;
    float r = texture(iChannel0, uv + vec2(bleed, 0.0)).r;
    float g = tex.g;
    float b = texture(iChannel0, uv - vec2(bleed, 0.0)).b;

    vec3 result = vec3(r, g, b) + noise + tracking;
    fragColor = vec4(result, tex.a);
}}
"""


def _shader_ethereal_glow(theme: AnimeTheme) -> str:
    """Soft ethereal glow. Used by: Frieren, Oshi no Ko."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Ethereal Glow
// Gentle, magical ambient glow

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Slowly shifting ambient light
    float wave1 = sin(uv.x * 3.0 + iTime * 0.5) * 0.5 + 0.5;
    float wave2 = sin(uv.y * 2.0 - iTime * 0.3) * 0.5 + 0.5;
    float ambient = wave1 * wave2;

    vec3 glowColor = {color};
    vec3 result = tex.rgb + glowColor * ambient * 0.08;

    // Soft top vignette
    float topGlow = smoothstep(1.0, 0.7, uv.y) * 0.05;
    result += glowColor * topGlow;

    fragColor = vec4(result, tex.a);
}}
"""


def _shader_cursed_energy(theme: AnimeTheme) -> str:
    """Pulsing dark energy. Used by: Jujutsu Kaisen."""
    color = _hex_to_vec3(theme.color_primary)
    accent = _hex_to_vec3(theme.color_accent)
    return f"""\
// Termisan Shader: {theme.name} — Cursed Energy
// Dark pulsing energy with occasional flares

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Pulsing dark overlay from edges
    vec2 center = uv - 0.5;
    float dist = length(center);
    float pulse = 0.5 + 0.5 * sin(iTime * 1.5);

    float energy = smoothstep(0.6, 0.3, dist) * 0.0;
    energy += smoothstep(0.05, 0.0, min(uv.x, 1.0 - uv.x)) * (0.2 + 0.1 * pulse);
    energy += smoothstep(0.05, 0.0, min(uv.y, 1.0 - uv.y)) * (0.2 + 0.1 * pulse);

    vec3 energyColor = mix({color}, {accent}, pulse);

    fragColor = vec4(tex.rgb + energyColor * energy, tex.a);
}}
"""


def _shader_pink_sparkle(theme: AnimeTheme) -> str:
    """Sparkle/glitter effect. Used by: Spy x Family."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Pink Sparkle
// Cute sparkle/glitter overlay

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Sparkles
    float sparkle = 0.0;
    for (int i = 0; i < 6; i++) {{
        float fi = float(i);
        vec2 pos = vec2(
            fract(sin(fi * 127.1) * 43758.5),
            fract(sin(fi * 311.7) * 43758.5)
        );
        // Slowly drift
        pos += vec2(sin(iTime * 0.5 + fi), cos(iTime * 0.3 + fi * 2.0)) * 0.05;
        pos = fract(pos);

        float dist = length(uv - pos);
        float twinkle = sin(iTime * 3.0 + fi * 1.7) * 0.5 + 0.5;
        sparkle += smoothstep(0.015, 0.0, dist) * twinkle * 0.4;
    }}

    vec3 sparkleColor = {color};
    fragColor = vec4(tex.rgb + sparkleColor * sparkle, tex.a);
}}
"""


def _shader_chainsaw_rev(theme: AnimeTheme) -> str:
    """Aggressive red pulse. Used by: Chainsaw Man."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Chainsaw Rev
// Aggressive pulsing red edges

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Fast aggressive pulse
    float pulse = abs(sin(iTime * 4.0));
    pulse = pow(pulse, 3.0);  // Sharp pulse

    // Edge glow
    float edgeDist = min(min(uv.x, 1.0 - uv.x), min(uv.y, 1.0 - uv.y));
    float edgeGlow = smoothstep(0.04, 0.0, edgeDist);

    vec3 glowColor = {color};
    float intensity = edgeGlow * pulse * 0.4;

    fragColor = vec4(tex.rgb + glowColor * intensity, tex.a);
}}
"""


def _shader_warm_parchment(theme: AnimeTheme) -> str:
    """Warm parchment tint. Used by: Apothecary Diaries, FMA."""
    color = _hex_to_vec3(theme.color_primary)
    return f"""\
// Termisan Shader: {theme.name} — Warm Parchment
// Subtle warm tint with aged paper feel

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Warm tint
    vec3 warmth = {color};
    vec3 result = mix(tex.rgb, tex.rgb * (vec3(1.0) + warmth * 0.1), 0.3);

    // Soft vignette
    vec2 center = uv - 0.5;
    float vignette = 1.0 - dot(center, center) * 0.5;
    result *= vignette;

    fragColor = vec4(result, tex.a);
}}
"""


def _shader_nen_aura(theme: AnimeTheme) -> str:
    """Nen aura effect. Used by: Hunter x Hunter."""
    color = _hex_to_vec3(theme.color_primary)
    accent = _hex_to_vec3(theme.color_accent)
    return f"""\
// Termisan Shader: {theme.name} — Nen Aura
// Flowing energy aura

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Flowing aura on edges
    float edgeDist = min(min(uv.x, 1.0 - uv.x), min(uv.y, 1.0 - uv.y));
    float flow = sin(uv.y * 10.0 + iTime * 2.0) * 0.5 + 0.5;
    flow *= sin(uv.x * 8.0 - iTime * 1.5) * 0.5 + 0.5;

    float aura = smoothstep(0.06, 0.0, edgeDist);
    vec3 auraColor = mix({color}, {accent}, flow);

    fragColor = vec4(tex.rgb + auraColor * aura * 0.3, tex.a);
}}
"""


def _shader_bankai(theme: AnimeTheme) -> str:
    """Dark energy release. Used by: Bleach."""
    accent = _hex_to_vec3(theme.color_secondary)
    return f"""\
// Termisan Shader: {theme.name} — Bankai
// Dark energy with bright accent flares

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;
    vec4 tex = texture(iChannel0, uv);

    // Dark overlay
    float darkness = smoothstep(0.5, 0.0, min(uv.x, 1.0 - uv.x)) * 0.1;

    // Accent energy lines from bottom
    float lines = 0.0;
    for (int i = 0; i < 3; i++) {{
        float fi = float(i);
        float x = fract(sin(fi * 43.7) * 4378.5);
        float lineX = abs(uv.x - x);
        float speed = 0.5 + fi * 0.3;
        float lineY = fract(uv.y + iTime * speed);
        lines += smoothstep(0.003, 0.0, lineX) * (1.0 - lineY) * 0.15;
    }}

    vec3 accentColor = {accent};
    vec3 result = tex.rgb - darkness + accentColor * lines;

    fragColor = vec4(result, tex.a);
}}
"""


def _shader_ocean_wave(theme: AnimeTheme) -> str:
    """Ocean wave effect. Used by: One Piece."""
    color = _hex_to_vec3(theme.color_accent)
    return f"""\
// Termisan Shader: {theme.name} — Ocean Wave
// Subtle wave distortion at the bottom

void mainImage(out vec4 fragColor, in vec2 fragCoord) {{
    vec2 uv = fragCoord.xy / iResolution.xy;

    // Wave at bottom
    float waveZone = smoothstep(0.1, 0.0, uv.y);
    float wave = sin(uv.x * 15.0 + iTime * 2.0) * 0.003 * waveZone;

    vec4 tex = texture(iChannel0, uv + vec2(0.0, wave));

    // Blue tint at bottom
    vec3 oceanColor = {color};
    vec3 result = tex.rgb + oceanColor * waveZone * 0.1;

    fragColor = vec4(result, tex.a);
}}
"""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# THEME → SHADER MAPPING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SHADER_GENERATORS: dict[str, callable] = {
    "dragonball": _shader_energy_aura,
    "onepiece": _shader_ocean_wave,
    "naruto": _shader_energy_aura,
    "aot": _shader_film_grain,
    "pokemon": _shader_bloom,
    "deathnote": _shader_dark_vignette,
    "fma": _shader_warm_parchment,
    "hxh": _shader_nen_aura,
    "bleach": _shader_bankai,
    "bebop": _shader_vhs_static,
    "demonslayer": _shader_flame_breathing,
    "jjk": _shader_cursed_energy,
    "mha": _shader_bloom,
    "spyfamily": _shader_pink_sparkle,
    "frieren": _shader_ethereal_glow,
    "oshinoko": _shader_ethereal_glow,
    "sololeveling": _shader_shadow_particles,
    "chainsawman": _shader_chainsaw_rev,
    "apothecary": _shader_warm_parchment,
    "cyberpunk": _shader_crt_glitch,
}


def generate_shader(theme_id: str) -> str | None:
    """Generate a GLSL shader string for the given theme ID."""
    if theme_id not in ALL_THEMES or theme_id not in SHADER_GENERATORS:
        return None
    theme = ALL_THEMES[theme_id]
    return SHADER_GENERATORS[theme_id](theme)


def install_shader(theme_id: str, config_dir: Path | None = None) -> Path | None:
    """Generate and write a shader file for the given theme.

    Args:
        theme_id: The theme to generate a shader for.
        config_dir: Ghostty config directory. Defaults to ~/.config/ghostty.

    Returns:
        Path to the written shader file, or None on failure.
    """
    shader_source = generate_shader(theme_id)
    if shader_source is None:
        return None

    if config_dir is None:
        config_dir = Path.home() / ".config" / "ghostty"

    shader_dir = config_dir / "shaders"
    shader_dir.mkdir(parents=True, exist_ok=True)

    shader_path = shader_dir / f"termisan-{theme_id}.glsl"
    shader_path.write_text(shader_source)
    return shader_path


def install_all_shaders(config_dir: Path | None = None) -> list[Path]:
    """Install shaders for all themes.

    Returns list of written shader file paths.
    """
    paths = []
    for theme_id in SHADER_GENERATORS:
        path = install_shader(theme_id, config_dir)
        if path:
            paths.append(path)
    return paths
