"""Accessible HTML diagrams built from read-only structure snapshots."""

from html import escape
from collections.abc import Sequence


DIAGRAM_CSS = """
<style>
.ds-diagram {background:#fff;border:1px solid #d7e2e5;border-radius:16px;
 padding:24px;min-height:190px;color:#192c3d;overflow:auto;max-height:520px;}
.ds-flow {display:flex;align-items:center;gap:14px;min-width:max-content;padding:8px;}
.ds-stack {display:flex;flex-direction:column;align-items:center;gap:10px;}
.ds-node {display:flex;flex-direction:column;align-items:center;gap:8px;}
.ds-value {border:2px solid #9dbdb8;border-radius:10px;padding:14px 22px;
 font:600 22px ui-monospace,monospace;max-width:240px;overflow-wrap:anywhere;
 background:#f1faf7;min-width:76px;text-align:center;}
.ds-stack .ds-value {min-width:170px;}
.ds-node:first-child .ds-value {border-color:#087f72;background:#e2f4ed;}
.ds-label {font-size:11px;font-weight:700;letter-spacing:1.4px;color:#35615d;min-height:16px;}
.ds-arrow {color:#526f7c;font-size:24px;}
.ds-pointer {border-left:1px solid #9dbdb8;padding-left:12px;margin-left:12px;color:#35615d;}
.ds-empty {padding:24px 0;text-align:center;color:#526f7c;}
.ds-null {font:600 18px ui-monospace,monospace;color:#526f7c;}
</style>
"""


def structure_diagram(kind: str, values: Sequence[object]) -> str:
    """Return escaped HTML for Stack, Queue, or Linked List in display order.

    Snapshots must be top-first, front-first, or head-first respectively.
    Does not mutate values. Raises ValueError for an unsupported kind.
    Runs in O(n) time and output space (plus value-string lengths).
    """
    if kind not in {"Stack", "Queue", "Linked List"}:
        raise ValueError(f"Unsupported structure: {kind}")
    orientation = {"Stack": "top to bottom", "Queue": "front to rear", "Linked List": "head to tail"}[kind]
    description = escape(f"{kind}, {orientation}: {list(values)}", quote=True)
    if not values:
        label = {"Stack": "TOP", "Queue": "FRONT / REAR", "Linked List": "HEAD → None"}[kind]
        content = f'<div class="ds-empty"><div class="ds-label">{label}</div><p>Empty {kind.lower()}. Add a value to begin.</p></div>'
    else:
        nodes = []
        for index, value in enumerate(values):
            if kind == "Stack":
                label = "TOP ↓" if index == 0 else ""
            elif kind == "Queue":
                label = "FRONT / REAR" if len(values) == 1 else "FRONT" if index == 0 else "REAR" if index == len(values) - 1 else ""
            else:
                label = "HEAD" if index == 0 else ""
            pointer = '<span class="ds-pointer">•</span>' if kind == "Linked List" else ""
            nodes.append(f'<div class="ds-node"><span class="ds-label">{label}</span><div class="ds-value">{escape(str(value))}{pointer}</div></div>')
        separator = '' if kind == "Stack" else '<span class="ds-arrow" aria-hidden="true">→</span>'
        content = separator.join(nodes)
        if kind == "Linked List":
            content += '<span class="ds-arrow" aria-hidden="true">→</span><span class="ds-null">None</span>'
        layout = "ds-stack" if kind == "Stack" else "ds-flow"
        content = f'<div class="{layout}">{content}</div>'
    return f'<section class="ds-diagram" role="img" aria-label="{description}">{content}</section>'
