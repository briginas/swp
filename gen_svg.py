#!/usr/bin/env python3
"""Generate the Sweep keymap SVG and draw.io diagrams."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from pathlib import Path


SVG_WIDTH = 820
LAYER_STEP_Y = 328
BOTTOM_MARGIN = 58
KEY_W = 48
KEY_H = 42
KEY_CENTER_X = KEY_W / 2
KEY_CENTER_Y = KEY_H / 2
ASSETS_DIR = Path(__file__).parent / "assets"
SVG_PATH = ASSETS_DIR / "sweep-layout.svg"
DRAWIO_PATH = ASSETS_DIR / "sweep-layout.drawio"


@dataclass(frozen=True)
class Key:
    label: str = ""
    sub: str = ""
    style: str = "normal"


@dataclass(frozen=True)
class Layer:
    id: str
    name: str
    bar: str
    note: str
    keys: list[Key]
    combo: str = ""


def k(label: str, sub: str = "", style: str = "normal") -> Key:
    return Key(label, sub, style)


def empty(label: str = "", sub: str = "") -> Key:
    return Key(label, sub, "empty")


KEY_POSITIONS = [
    (80, 110, 0), (132, 85, 0), (184, 70, 0), (236, 85, 0), (288, 93, 0),
    (484, 93, 0), (536, 85, 0), (588, 70, 0), (640, 85, 0), (692, 110, 0),
    (80, 156, 0), (132, 131, 0), (184, 116, 0), (236, 131, 0), (288, 139, 0),
    (484, 139, 0), (536, 131, 0), (588, 116, 0), (640, 131, 0), (692, 156, 0),
    (80, 202, 0), (132, 177, 0), (184, 162, 0), (236, 177, 0), (288, 185, 0),
    (484, 185, 0), (536, 177, 0), (588, 162, 0), (640, 177, 0), (692, 202, 0),
    (258, 248, 15), (314, 267, 30), (458, 267, -30), (514, 248, -15),
]


LAYERS = [
    Layer(
        id="base-layer",
        name="Base",
        bar="bar-base",
        note="QWERTY with balanced home row mods",
        combo="Combos: D+K Esc | A+; Caps | E+I Lang | U+P Adj L | Q+R Adj R | Z+/ Plain",
        keys=[
            k("Q"), k("W"), k("E"), k("R"), k("T"),
            k("Y"), k("U"), k("I"), k("O"), k("P"),
            k("A", "Sft"), k("S", "Ctl"), k("D", "Gui"), k("F", "Alt"), k("G"),
            k("H"), k("J", "Alt"), k("K", "Gui"), k("L", "Ctl"), k(";", "Sft"),
            k("Z"), k("X"), k("C"), k("V"), k("B"),
            k("N"), k("M"), k(","), k("."), k("/"),
            k("Sym", style="layer-red"), k("Space", style="special"),
            k("Enter", style="special"), k("Nav", style="layer-gold"),
        ],
    ),
    Layer(
        id="symbols-layer",
        name="Symbols",
        bar="bar-sym",
        note="Hold left thumb from Base",
        keys=[
            k("!"), k("@"), k("#"), k("$"), k("%"),
            empty(), k("&"), k("*"), k("("), k(")"),
            k("Esc", "Sft", "special"), k("LCtl"), k("LGui"), k("LAlt"), k("^"),
            k("-"), k("=", "Alt"), k("{", "Gui"), k("}", "Ctl"), k("'", "Sft"),
            k("Tab", style="special"), empty(), empty(), empty(), empty(),
            empty(), k("Bspc", style="special"), k("["), k("]"), k("\\"),
            empty(), empty(), empty(), empty(),
        ],
    ),
    Layer(
        id="nav-layer",
        name="Nav",
        bar="bar-nav",
        note="Hold right thumb from Base",
        keys=[
            k("1"), k("2"), k("3"), k("4"), k("5"),
            k("6"), k("7"), k("8"), k("9"), k("0"),
            k("LSft"), k("LCtl"), k("LGui"), k("LAlt"), k("6"),
            k("Left", style="special"), k("Down", "Alt", "special"), k("Up", "Gui", "special"),
            k("Right", "Ctl", "special"), k("RSft"),
            k("`"), empty(), empty(), k("Del", style="special"), empty(),
            empty(), empty(), empty(), empty(), empty(),
            empty(), empty(), empty(), empty(),
        ],
    ),
    Layer(
        id="adjust-left-layer",
        name="Adjust L",
        bar="bar-adj",
        note="Hold U+P combo",
        keys=[
            k("F1"), k("F2"), k("F3"), k("F4"), empty(),
            empty(), empty(), empty(), empty(), empty(),
            k("F5"), k("F6"), k("F7"), k("F8"), empty(),
            empty(), empty(), empty(), empty(), empty(),
            k("F9"), k("F10"), k("F11"), k("F12"), empty(),
            empty(), empty(), empty(), empty(), empty(),
            empty(), empty(), empty(), empty(),
        ],
    ),
    Layer(
        id="adjust-right-layer",
        name="Adjust R",
        bar="bar-adj",
        note="Hold Q+R combo",
        keys=[
            empty(), empty(), empty(), empty(), empty(),
            empty(), empty(), empty(), empty(), empty(),
            empty(), empty(), empty(), empty(), empty(),
            empty(), k("Vol-", style="special"), k("Mute", style="special"), k("Vol+", style="special"), empty(),
            empty(), empty(), empty(), empty(), empty(),
            k("BT", "0", "layer-blue"), k("Prev", style="special"), k("Play", style="special"),
            k("Next", style="special"), k("BT", "CLR", "layer-blue"),
            empty(), empty(), empty(), empty(),
        ],
    ),
    Layer(
        id="plain-base-layer",
        name="Base plain",
        bar="bar-base",
        note="Toggle Z+/ combo; QWERTY without home row mods",
        keys=[
            k("Q"), k("W"), k("E"), k("R"), k("T"),
            k("Y"), k("U"), k("I"), k("O"), k("P"),
            k("A"), k("S"), k("D"), k("F"), k("G"),
            k("H"), k("J"), k("K"), k("L"), k(";"),
            k("Z"), k("X"), k("C"), k("V"), k("B"),
            k("N"), k("M"), k(","), k("."), k("/"),
            k("Sym", style="layer-red"), k("Space", style="special"),
            k("Enter", style="special"), k("Nav", style="layer-gold"),
        ],
    ),
]


STYLE_TO_USE = {
    "normal": "key-normal",
    "special": "key-special",
    "empty": "key-empty",
    "layer-red": "key-layer-red",
    "layer-gold": "key-layer-gold",
    "layer-blue": "key-layer-blue",
}


DRAWIO_STYLE = {
    "normal": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#383e47;strokeColor=#05070a;fontColor=#edf2f7;fontStyle=1;fontSize=13;align=center;verticalAlign=middle;",
    "special": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#495566;strokeColor=#121820;fontColor=#edf2f7;fontStyle=1;fontSize=11;align=center;verticalAlign=middle;",
    "empty": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#202833;strokeColor=#596170;dashed=1;dashPattern=4 4;fontColor=#edf2f7;fontStyle=1;fontSize=10;align=center;verticalAlign=middle;",
    "layer-red": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#a20025;strokeColor=#6f0000;fontColor=#edf2f7;fontStyle=1;fontSize=13;align=center;verticalAlign=middle;",
    "layer-gold": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#d9a725;strokeColor=#b08312;fontColor=#111820;fontStyle=1;fontSize=13;align=center;verticalAlign=middle;",
    "layer-blue": "rounded=1;whiteSpace=wrap;html=1;arcSize=12;fillColor=#5c8cca;strokeColor=#456893;fontColor=#111820;fontStyle=1;fontSize=11;align=center;verticalAlign=middle;",
}


def svg_height() -> int:
    return len(LAYERS) * LAYER_STEP_Y + BOTTOM_MARGIN


def assert_layout() -> None:
    expected = len(KEY_POSITIONS)
    for layer in LAYERS:
        if len(layer.keys) != expected:
            raise ValueError(f"{layer.id} has {len(layer.keys)} keys, expected {expected}")


def text_class(key: Key) -> str:
    if key.style in {"layer-gold", "layer-blue"}:
        return "key-text-dark-small" if key.sub or len(key.label) > 3 else "key-text-dark"
    if key.style == "special" and len(key.label) > 3:
        return "key-text-small"
    if len(key.label) > 3:
        return "key-text-small"
    return "key-text"


def svg_key(key: Key, x: int, y: int, rotation: int) -> str:
    transform = f"translate({x} {y})"
    if rotation:
        transform += f" rotate({rotation} {KEY_CENTER_X:g} {KEY_CENTER_Y:g})"

    label = escape(key.label)
    sub = escape(key.sub)
    use = STYLE_TO_USE[key.style]
    if not key.label:
        text = ""
    elif key.sub:
        text = (
            f'<text class="{text_class(key)}" x="{KEY_CENTER_X:g}" y="17">{label}</text>'
            f'<text class="key-sub" x="{KEY_CENTER_X:g}" y="30">{sub}</text>'
        )
    else:
        text = f'<text class="{text_class(key)}" x="{KEY_CENTER_X:g}" y="{KEY_CENTER_Y:g}">{label}</text>'

    return f'    <g transform="{transform}"><use href="#{use}"/>{text}</g>'


def svg_layer(layer: Layer, offset_y: int) -> str:
    lines = [
        f'  <g id="{layer.id}" transform="translate(0 {offset_y})">',
        '    <rect class="layer-panel" x="32" y="12" width="756" height="336" rx="8" ry="8"/>',
        f'    <rect class="{layer.bar}" x="305" y="28" width="210" height="30" rx="4" ry="4"/>',
        f'    <text class="title-text" x="410" y="43">{escape(layer.name)}</text>',
        f'    <text class="note-text" x="410" y="72">{escape(layer.note)}</text>',
        "",
    ]
    for idx, key in enumerate(layer.keys):
        x, y, rotation = KEY_POSITIONS[idx]
        lines.append(svg_key(key, x, y, rotation))
        if idx in {9, 19, 29}:
            lines.append("")
    if layer.combo:
        lines.append(f'    <text class="combo-text" x="410" y="314">{escape(layer.combo)}</text>')
    lines.append("  </g>")
    return "\n".join(lines)


def generate_svg() -> str:
    assert_layout()
    layers = "\n\n".join(svg_layer(layer, idx * LAYER_STEP_Y) for idx, layer in enumerate(LAYERS))
    height = svg_height()
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{height}" viewBox="0 0 {SVG_WIDTH} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Sweep keymap layout</title>
  <desc id="desc">Six-layer layout diagram for the Sweep-style cradio ZMK keymap.</desc>
  <defs>
    <g id="key-normal">
      <rect class="key-normal" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-red">
      <rect class="key-layer-red" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-gold">
      <rect class="key-layer-gold" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-layer-blue">
      <rect class="key-layer-blue" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-special">
      <rect class="key-special" width="48" height="42" rx="6" ry="6"/>
    </g>
    <g id="key-empty">
      <rect class="key-empty" width="48" height="42" rx="6" ry="6"/>
    </g>
    <style>
      .sheet {{ fill: #10141b; }}
      .layer-panel {{ fill: #151b24; stroke: #293241; stroke-width: 1; }}
      .bar-base {{ fill: #3f4a59; stroke: #556173; }}
      .bar-sym {{ fill: #a20025; stroke: #6f0000; }}
      .bar-nav {{ fill: #d9a725; stroke: #b08312; }}
      .bar-adj {{ fill: #5c8cca; stroke: #456893; }}
      .key-normal {{ fill: #383e47; stroke: #05070a; stroke-width: 1; }}
      .key-layer-red {{ fill: #a20025; stroke: #6f0000; stroke-width: 1; }}
      .key-layer-gold {{ fill: #d9a725; stroke: #b08312; stroke-width: 1; }}
      .key-layer-blue {{ fill: #5c8cca; stroke: #456893; stroke-width: 1; }}
      .key-special {{ fill: #495566; stroke: #121820; stroke-width: 1; }}
      .key-empty {{ fill: #202833; stroke: #596170; stroke-width: 1; stroke-dasharray: 4 4; }}
      .title-text {{ fill: #ffffff; font: 700 16px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .note-text {{ fill: #aeb9c8; font: 12px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text {{ fill: #edf2f7; font: 700 15px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-dark {{ fill: #111820; font: 700 14px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-small {{ fill: #edf2f7; font: 700 10px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-text-dark-small {{ fill: #111820; font: 700 10px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .key-sub {{ fill: #9fb0c3; font: 700 8.5px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
      .combo-text {{ fill: #7ea6e0; font: 12px Verdana, Arial, sans-serif; text-anchor: middle; dominant-baseline: middle; }}
    </style>
  </defs>

  <rect class="sheet" width="{SVG_WIDTH}" height="{height}"/>

{layers}
</svg>
'''


def drawio_cell(cell_id: int, value: str, style: str, x: float, y: float, w: float, h: float) -> str:
    return (
        f'        <mxCell id="{cell_id}" value="{escape(value)}" style="{style}" vertex="1" parent="1">\n'
        f'          <mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry" />\n'
        "        </mxCell>"
    )


def drawio_key_value(key: Key) -> str:
    if not key.label:
        return ""
    if key.sub:
        return f"{key.label}<br>{key.sub}"
    return key.label


def generate_drawio() -> str:
    assert_layout()
    height = svg_height()
    cells = [
        '        <mxCell id="0" />',
        '        <mxCell id="1" parent="0" />',
    ]
    cell_id = 2
    sheet_style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#10141b;strokeColor=none;"
    cells.append(drawio_cell(cell_id, "", sheet_style, 0, 0, SVG_WIDTH, height))
    cell_id += 1

    for layer_index, layer in enumerate(LAYERS):
        offset_y = layer_index * LAYER_STEP_Y
        cells.append(drawio_cell(cell_id, "", "rounded=1;whiteSpace=wrap;html=1;fillColor=#151b24;strokeColor=#293241;fontColor=#ffffff;", 32, offset_y + 12, 756, 336))
        cell_id += 1
        bar_style = {
            "bar-base": "rounded=1;whiteSpace=wrap;html=1;fillColor=#3f4a59;strokeColor=#556173;fontColor=#ffffff;fontStyle=1;fontSize=16;align=center;verticalAlign=middle;",
            "bar-sym": "rounded=1;whiteSpace=wrap;html=1;fillColor=#a20025;strokeColor=#6f0000;fontColor=#ffffff;fontStyle=1;fontSize=16;align=center;verticalAlign=middle;",
            "bar-nav": "rounded=1;whiteSpace=wrap;html=1;fillColor=#d9a725;strokeColor=#b08312;fontColor=#111820;fontStyle=1;fontSize=16;align=center;verticalAlign=middle;",
            "bar-adj": "rounded=1;whiteSpace=wrap;html=1;fillColor=#5c8cca;strokeColor=#456893;fontColor=#ffffff;fontStyle=1;fontSize=16;align=center;verticalAlign=middle;",
        }[layer.bar]
        cells.append(drawio_cell(cell_id, "", bar_style, 305, offset_y + 28, 210, 30))
        cell_id += 1
        cells.append(drawio_cell(cell_id, layer.name, bar_style, 370, offset_y + 33, 80, 20))
        cell_id += 1
        cells.append(drawio_cell(cell_id, layer.note, "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#aeb9c8;fontSize=12;", 250, offset_y + 62, 320, 20))
        cell_id += 1

        for idx, key in enumerate(layer.keys):
            x, y, rotation = KEY_POSITIONS[idx]
            style = DRAWIO_STYLE[key.style]
            if rotation:
                style += f"rotation={float(rotation):.1f};"
            cells.append(drawio_cell(cell_id, drawio_key_value(key), style, x, offset_y + y, KEY_W, KEY_H))
            cell_id += 1

        if layer.combo:
            cells.append(drawio_cell(cell_id, layer.combo, "text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;fontColor=#7ea6e0;fontSize=12;", 140, offset_y + 304, 540, 20))
            cell_id += 1

    body = "\n".join(cells)
    return f'''<mxfile host="app.diagrams.net" agent="zmk-sweep" version="24.7.0" type="device">
  <diagram id="sweep-layout" name="sweep-layout">
    <mxGraphModel dx="1180" dy="760" grid="1" gridSize="10" guides="1" tooltips="1" connect="0" arrows="1" fold="1" page="1" pageScale="1" pageWidth="850" pageHeight="{height + 30}" math="0" shadow="0">
      <root>
{body}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
'''


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(generate_svg(), encoding="utf-8")
    DRAWIO_PATH.write_text(generate_drawio(), encoding="utf-8")


if __name__ == "__main__":
    main()
