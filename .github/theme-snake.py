#!/usr/bin/env python3
"""Re-theme the Platane/snk contribution snake as a Christmas scene.

Runs in the profile repo's workflow right after snk generates its SVG, so the
snake stays live (new contributions keep getting eaten) *and* stays themed.

  python3 .github/theme-snake.py dist/snake.svg

What it changes:
  * palette    -> ice blues for the contribution blocks, snow-white high end
  * snake      -> snow-white snowball chain with a frosty edge
  * snowfall   -> a handful of drifting snowflakes (pure CSS, no JS)
"""
import re
import sys

MARKER = "christmas-theme"

ICE_PALETTE = (
    "--cb:#3a6ea533;"
    "--cs:#ffffff;"
    "--ce:#0d1f33;"
    "--c0:#0d1f33;"
    "--c1:#1f6fb2;"
    "--c2:#3aa0e0;"
    "--c3:#8fd0f5;"
    "--c4:#eaf7ff"
)

EXTRA_CSS = f"""
/* {MARKER} */
.s{{stroke:#6fb7e8;stroke-width:1.1px;stroke-linejoin:round}}
.c{{stroke:var(--cb)}}
/* the head decoration rides the same animation as the leading segment (s0) */
.head-deco{{animation:none linear 37300ms infinite;animation-name:s0;fill:none;pointer-events:none}}
@keyframes snow-fall{{0%{{transform:translateY(-46px)}}100%{{transform:translateY(198px)}}}}
@keyframes snow-sway{{0%,100%{{transform:translateX(0)}}50%{{transform:translateX(6px)}}}}
.snowflake{{fill:#eaf7ff;animation:snow-fall linear infinite,snow-sway ease-in-out infinite}}
"""

# A Santa hat + two eyes, authored in the head cell's 16x16 coordinate space.
# Uses the s0 animation so it stays glued to the leading segment.
HEAD_SVG = (
    '<g class="head-deco" aria-hidden="true">'
    # hat cone + pom-pom + white trim
    '<path d="M3.1 3.4 L7.9 -6.4 L12.9 3.4 Z" fill="#e23636"/>'
    '<circle cx="7.9" cy="-7.0" r="2.5" fill="#ffffff"/>'
    '<rect x="1.9" y="2.3" width="12.2" height="2.7" rx="1.35" fill="#ffffff"/>'
    # eyes (frosty dark) + tiny rosy cheeks
    '<circle cx="5.5" cy="8.4" r="1.6" fill="#12233a"/>'
    '<circle cx="10.5" cy="8.4" r="1.6" fill="#12233a"/>'
    '<circle cx="4.3" cy="10.6" r="1.0" fill="#ff9bb3" opacity="0.85"/>'
    '<circle cx="11.7" cy="10.6" r="1.0" fill="#ff9bb3" opacity="0.85"/>'
    "</g>"
)

# cx, r, fall-duration, delay, opacity, sway-duration
FLAKES = [
    (24, 2.2, 9.0, 0.0, 0.85, 3.1),
    (78, 1.6, 11.5, 2.1, 0.55, 4.2),
    (132, 2.6, 8.0, 4.4, 0.9, 2.7),
    (186, 1.4, 12.5, 1.2, 0.5, 5.0),
    (240, 2.0, 9.8, 5.6, 0.75, 3.6),
    (296, 1.7, 10.6, 3.0, 0.6, 4.0),
    (352, 2.4, 8.6, 6.8, 0.85, 2.9),
    (408, 1.5, 11.9, 0.6, 0.55, 4.6),
    (462, 2.1, 9.2, 4.0, 0.8, 3.3),
    (518, 1.6, 12.1, 2.6, 0.5, 4.8),
    (572, 2.5, 8.2, 5.2, 0.9, 2.6),
    (628, 1.5, 10.9, 1.8, 0.55, 4.3),
    (684, 2.2, 9.5, 6.4, 0.8, 3.0),
    (740, 1.7, 11.3, 3.6, 0.6, 4.5),
    (796, 2.3, 8.9, 0.9, 0.85, 3.4),
    (838, 1.5, 12.3, 5.0, 0.5, 5.2),
]


def theme(svg: str) -> str:
    if MARKER in svg:
        return svg  # already themed

    # 1. swap the colour palette
    svg = re.sub(r":root\{[^}]*\}", ":root{" + ICE_PALETTE + "}", svg, count=1)

    # 2. append the extra CSS inside the existing <style>
    svg = svg.replace("</style>", EXTRA_CSS + "</style>", 1)

    # 3. sprinkle snowflakes on top of everything
    flakes = "".join(
        f'<circle class="snowflake" cx="{x}" cy="-6" r="{r}" opacity="{op}" '
        f'style="animation-duration:{dur}s,{sway}s;animation-delay:-{delay}s,0s"/>'
        for x, r, dur, delay, op, sway in FLAKES
    )
    svg = svg.replace("</svg>", f'<g aria-hidden="true">{flakes}</g></svg>', 1)

    # 4. Santa hat + eyes on the leading segment
    svg = add_head(svg)
    return svg


def add_head(svg: str) -> str:
    """Glue a Santa hat + eyes onto the leading snake segment (class s0)."""
    if 'class="head-deco"' in svg:
        return svg
    # s0 is the first <rect class="s s0" .../> in document order
    svg = re.sub(r'(<rect class="s s0"[^>]*>)', r'\1' + HEAD_SVG, svg, count=1)
    return svg


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "dist/snake.svg"
    with open(path, encoding="utf-8") as handle:
        src = handle.read()
    out = theme(src)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(out)
    print(f"themed {path}: {len(src)} -> {len(out)} bytes")


if __name__ == "__main__":
    main()
